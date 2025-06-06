from typing import Sequence
from fastapi import APIRouter, Depends
from requests import Session
from app.core.database import get_db
from app.models.user_models import UserCreate, UserRead, UserDelete, UserLoginCreate, UserLoginRead
from app.schemas.user import User
from app.services.api_key_service import verify_api_key
from app.services.auth_service import AppwriteAuthService, get_auth_service
from app.services.user_services import create_user, get_user_by_email, get_users, delete_user, login_user
from app.models.auth_models import EmailVerificationRequest, EmailRequest
from appwrite.exception import AppwriteException
from fastapi import HTTPException

users_router = APIRouter()


# Get all users
@users_router.get("/")
async def get_users_route(db: Session = Depends(get_db), api_key=Depends(verify_api_key)) -> Sequence[User]:
    return get_users(db)


# Get a user by email
@users_router.get("/email/{user_email}")
async def get_user_route(user_email: str, db: Session = Depends(get_db), _=Depends(verify_api_key)) -> User | None:
    return get_user_by_email(db, user_email)

@users_router.post("/send-verification")
def send_verify_email(
    user: EmailRequest,
    auth: AppwriteAuthService = Depends(get_auth_service),
    _=Depends(verify_api_key)
):
    message = auth.send_verification_email(user)
    return message

@users_router.get("/verify-email")
def verify_email(
        user: EmailVerificationRequest,
        auth: AppwriteAuthService = Depends(get_auth_service),
        _=Depends(verify_api_key)
):
    message = auth.verify_email(user)
    return message


# Create a user
@users_router.post("/", response_model=UserRead)
async def register_user_route(
        user: UserCreate,
        db: Session = Depends(get_db),
        auth: AppwriteAuthService = Depends(get_auth_service),
        _=Depends(verify_api_key)
) -> UserRead:
    return create_user(db, user, auth)


# Delete a user
@users_router.delete("/{user_id}")
async def delete_user_route(
        user: UserDelete,
        db: Session = Depends(get_db),
        auth: AppwriteAuthService = Depends(get_auth_service),
        _=Depends(verify_api_key)
) -> UserRead:
    return delete_user(db, user, auth)

# Login a user
@users_router.post("/login")
async def login_user_route(
        user: UserLoginCreate,
        db: Session = Depends(get_db),
        auth: AppwriteAuthService = Depends(get_auth_service),
        _=Depends(verify_api_key)
) -> UserLoginRead:
    return login_user(db, user, auth)
