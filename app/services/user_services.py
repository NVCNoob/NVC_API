from typing import Sequence, Optional, cast
from sqlmodel import Session, select
from sqlmodel.sql._expression_select_cls import Select
from app.core.security import hash_password
from app.models.user_models import UserCreate, UserRead
from app.schemas.user import User


def create_user(db: Session, user_create: UserCreate) -> UserRead:
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

def delete_user(db: Session, user_id: int) -> User:
    statement: Select = cast(Select, select(User).where(User.id == user_id))
    user = db.exec(statement).first()
    db.delete(user)
    db.commit()
    return user



