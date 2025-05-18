from fastapi import APIRouter, Depends
from requests import Session
from app.core.database import get_db
from app.models.user_models import UserCreate, UserRead
from app.services.user_services import create_user, get_user_by_email, get_users, delete_user

users_router = APIRouter()


# Get all users
@users_router.get("/")
async def get_users_route(db: Session = Depends(get_db)):
    return get_users(db)


# Get a user by email
@users_router.get("/email/{user_email}")
async def get_user_route(user_email: str, db: Session = Depends(get_db)):
    return get_user_by_email(db, user_email)


# Create a user
@users_router.post("/", response_model=UserRead)
def register_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


# Delete a user
@users_router.delete("/{user_id}")
async def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)
