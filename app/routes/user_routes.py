from fastapi import APIRouter, Depends
from requests import Session
from app.core.database import get_db
from app.models.user_models import UserCreate, UserRead, UserDelete, UserLoginCreate
from app.services.api_key_service import verify_api_key
from app.services.auth_service import AppwriteAuthService, get_auth_service
from app.services.user_services import create_user, get_user_by_email, get_users, delete_user, login_user

users_router = APIRouter()


# Get all users
@users_router.get("/")
async def get_users_route(db: Session = Depends(get_db), api_key=Depends(verify_api_key)):
    return get_users(db)


# Get a user by email
@users_router.get("/email/{user_email}")
async def get_user_route(user_email: str, db: Session = Depends(get_db), _=Depends(verify_api_key)):
    return get_user_by_email(db, user_email)


# Create a user
@users_router.post("/", response_model=UserRead)
def register_user_route(
        user: UserCreate,
        db: Session = Depends(get_db),
        auth: AppwriteAuthService = Depends(get_auth_service),
        _=Depends(verify_api_key)
):
    return create_user(db, user, auth)


# Delete a user
@users_router.delete("/{user_id}")
async def delete_user_route(
        user: UserDelete,
        db: Session = Depends(get_db),
        auth: AppwriteAuthService = Depends(get_auth_service),
        _=Depends(verify_api_key)
):
    return delete_user(db, user, auth)

# Login a user
@users_router.delete("/login")
async def login_user_route(
        user: UserLoginCreate,
        db: Session = Depends(get_db),
        auth: AppwriteAuthService = Depends(get_auth_service),
        _=Depends(verify_api_key)
):
    return login_user(db, user, auth)
