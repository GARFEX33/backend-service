from uuid import uuid4, UUID
from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Ubicacion(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    ubicacion: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = {"arbitrary_types_allowed": True}