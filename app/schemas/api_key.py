from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid

class APIKey(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str  # e.g., "Fyne Desktop Client"
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    revoked_at: Optional[datetime] = None
