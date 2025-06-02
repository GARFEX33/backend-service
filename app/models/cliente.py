from typing import Optional
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class Cliente(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    nombre: str = Field(unique=True)
    created_at: datetime = Field(default_factory=datetime.now)