from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    phone_number: str
    nin: str

class UserDelete(BaseModel):
    id: int
    jwt: str

#nciedf
class UserRead(BaseModel):
    id: int
    name: str
    email: str
    nin: Optional[str]
    is_active: bool
    phone_number: str = None
    is_verified: bool = False
    created_at: datetime

    model_config = {
        "from_attributes": True,  # Enables ORM mode in Pydantic v2
    }

class UserLoginCreate(BaseModel):
    email: str
    password: str

class UserLoginRead(BaseModel):
    id: int
    name: str
    email: str
    nin: str
    is_active: bool
    phone_number: str = None
    is_verified: bool = False
    created_at: datetime
    jwt: str

    model_config = {
        "from_attributes": True,  # Enables ORM mode in Pydantic v2
    }
