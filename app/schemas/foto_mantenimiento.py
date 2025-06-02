from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class FotoMantenimientoCreate(BaseModel):
    categoria: str
    url: str
    nombre: str
    equipos_mantenimiento_id: UUID

class FotoMantenimientoUpdate(BaseModel):
    categoria: Optional[str] = None
    url: Optional[str] = None
    nombre: Optional[str] = None
    equipos_mantenimiento_id: Optional[UUID] = None

class FotoMantenimientoRead(BaseModel):
    id: UUID
    created_at: datetime
    categoria: str
    url: str
    nombre: str
    equipos_mantenimiento_id: UUID

class FotoMantenimientoResponse(BaseModel):
    id: UUID
    created_at: datetime
    categoria: str
    url: str
    nombre: str
    equipos_mantenimiento_id: UUID

class FotoUploadResponse(BaseModel):
    id: UUID
    url: str
    categoria: str
    nombre: str