from typing import Optional
from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from app.schemas.types import NombreCliente

class ClienteCreate(BaseModel):
    nombre: str  = Field(..., json_schema_extra={"example": "Juan Pérez"}, description="Nombre único del cliente. No se permiten duplicados")

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, json_schema_extra={"example": "Juan Pérez Actualizado"}, description="Nombre único del cliente. No se permiten duplicados")

class ClienteRead(BaseModel):
    id: UUID4
    nombre: str
    created_at: datetime

    class Config:
        orm_mode = True



class ClienteResponse(BaseModel):
    status: str = "success"
    data: ClienteRead
    message: str = "Success"