from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class MantenimientoGeneralCreate(BaseModel):
    cliente_id: UUID
    ubicacion_id: UUID
    periodo: str

class MantenimientoGeneralUpdate(BaseModel):
    cliente_id: Optional[UUID] = None
    ubicacion_id: Optional[UUID] = None
    periodo: Optional[str] = None

class MantenimientoGeneralRead(BaseModel):
    id: UUID
    cliente_id: UUID
    ubicacion_id: UUID
    periodo: str
    created_at: datetime

    class Config:
        orm_mode = True

class MantenimientoGeneralResponse(BaseModel):
    id: UUID
    cliente_id: UUID
    ubicacion_id: UUID
    periodo: str
    created_at: datetime

    class Config:
        orm_mode = True