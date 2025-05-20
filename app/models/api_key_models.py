from pydantic import BaseModel


class APIKeyCreate(BaseModel):
    name: str

class APIKeyRead(BaseModel):
    api_key: str
    name: str