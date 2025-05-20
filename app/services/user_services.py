from typing import Sequence, Optional, cast
from appwrite.exception import AppwriteException
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session, select
from sqlmodel.sql._expression_select_cls import Select
from app.core.security import hash_password
from app.models.user_models import UserCreate, UserRead, UserDelete, UserLoginCreate, UserLoginRead
from app.schemas.user import User
from app.services.auth_service import AppwriteAuthService


def create_user(db: Session, user_create: UserCreate, auth: AppwriteAuthService) -> UserRead:
    # Optional: Check if the user exists in local DB first
    existing_user = get_user_by_email(db, user_create.email)
    if existing_user:
        raise HTTPException(status_code=409, detail="User with this email already exists")

    # Try to create user on Appwrite
    try:
        auth.signup_user(user_create.email, user_create.password)
    except AppwriteException as e:
        if e.code == 409:
            raise HTTPException(status_code=409, detail="User already exists on Appwrite")
        raise HTTPException(status_code=500, detail=f"Appwrite error: {e.message}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error during Appwrite signup: {str(e)}")

    # Create user locally
    try:
        user = User(
            name=user_create.name,
            email=user_create.email,
            phone_number=user_create.phone_number,
            password=hash_password(user_create.password),
            nin=user_create.nin,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return UserRead.model_validate(user)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def get_users(db: Session) -> Sequence[User]:
    statement = select(User)
    results = db.exec(statement)
    return results.all()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    statement: Select = cast(Select, select(User).where(User.email == email))
    results = db.exec(statement)
    return results.first()


def delete_user(db: Session, user_delete: UserDelete, auth: AppwriteAuthService) -> UserRead:
    # Delete the Appwrite account using the JWT
    try:
        auth.delete_user_account(user_delete.jwt)
    except AppwriteException as e:
        raise HTTPException(status_code=400, detail=f"Appwrite deletion failed: {e.message}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error deleting Appwrite account: {str(e)}")

    # Query the local DB for the user
    statement: Select = cast(Select, select(User).where(User.id == user_delete.user_id))
    user = db.exec(statement).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found in local database")

    # Delete user from local DB
    db.delete(user)
    db.commit()

    return UserRead.model_validate(user)


def login_user(db: Session, user: UserLoginCreate, auth: AppwriteAuthService) -> UserLoginRead:
    try:
        jwt = auth.login_user(user.email, user.password)
        user = get_user_by_email(db, user.email)

        user = UserLoginRead(
            id = user.id,
            name = user.name,
            email = user.email,
            phone_number = user.phone_number,
            nin = user.nin,
            is_verified = user.is_verified,
            is_active = user.is_active,
            created_at = user.created_at,
            jwt = jwt,
        )

        return UserLoginRead.model_validate(user)
    except AppwriteException as e:
        if e.code == 401:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        raise HTTPException(status_code=500, detail=f"Appwrite error: {e.message}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected login error: {str(e)}")

