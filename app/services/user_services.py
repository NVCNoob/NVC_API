from typing import Sequence, Optional, cast
from sqlmodel import Session, select
from sqlmodel.sql._expression_select_cls import Select
from app.core.security import hash_password
from app.models.user_models import UserCreate, UserRead, UserDelete
from app.schemas.user import User
from app.services.auth_service import AppwriteAuthService


def create_user(db: Session, user_create: UserCreate, auth: AppwriteAuthService) -> UserRead:
    appwrite_user = auth.signup_user(user_create.email, user_create.password)

    user = User(
        name=user_create.name,
        email=user_create.email,
        password=hash_password(user_create.password),
        nin=user_create.nin,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return UserRead.model_validate(user)


def get_users(db: Session) -> Sequence[User]:
    statement = select(User)
    results = db.exec(statement)
    return results.all()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    statement: Select = cast(Select, select(User).where(User.email == email))
    results = db.exec(statement)
    return results.first()

def delete_user(db: Session, user_delete: UserDelete, auth: AppwriteAuthService) -> User:
    # Delete the Appwrite account using the JWT
    try:
        auth.delete_user_account(user_delete.jwt)
    except Exception as e:
        raise Exception(f"Failed to delete Appwrite account: {e}")

    # Query the local DB for the user
    statement: Select = cast(Select, select(User).where(User.id == user_delete.user_id))
    user = db.exec(statement).first()

    if not user:
        raise Exception("User not found in local database")

    # Delete it from the local DB
    db.delete(user)
    db.commit()
    return user.model_validate()



def login_user(auth: AppwriteAuthService, email: str, password: str) -> str:
    return auth.login_user(email, password)
