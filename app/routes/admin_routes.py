from fastapi import APIRouter, Depends
from sqlmodel import Session
from uuid import uuid4
from app.core.database import get_db
from app.models.api_key_models import APIKeyCreate, APIKeyRead
from app.schemas.api_key import APIKey
from app.services.api_key_service import admin_only

admin_router = APIRouter()

@admin_router.post("/create-api-key")
async def create_api_key(api_key: APIKeyCreate, db: Session = Depends(get_db), _=Depends(admin_only)) -> APIKeyRead:
    key_str = str(uuid4())

    api_key = APIKey(
        key=key_str,
        name=api_key.name,
        is_active=True
    )

    db.add(api_key)
    db.commit()
    db.refresh(api_key)

    return APIKeyRead(api_key=api_key.key, name=api_key.name)
