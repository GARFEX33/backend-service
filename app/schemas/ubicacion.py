from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class UbicacionCreate(BaseModel):
    ubicacion: str

class UbicacionUpdate(BaseModel):
    ubicacion: Optional[str] = None

class UbicacionRead(BaseModel):
    id: UUID
    ubicacion: str
    created_at: datetime