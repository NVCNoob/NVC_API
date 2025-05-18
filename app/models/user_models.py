from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    phone_number: str = None
    nin: str

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    nin: str
    is_active: bool
    phone_number: str = None
    is_verified: bool = False
    created_at: datetime

    model_config = {
        "from_attributes": True,  # Enables ORM mode in Pydantic v2
    }
