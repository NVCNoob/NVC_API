from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, UTC


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str
    phone_number: str
    nin: str
    is_verified: bool = False
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
