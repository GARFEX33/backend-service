from pydantic import BaseModel, Field, UUID4, ConfigDict
from typing import Optional, Dict
from uuid import UUID
from datetime import datetime

class EquipoMantenimientoCreate(BaseModel):
    equipo: str = Field(..., min_length=3, max_length=50, json_schema_extra={"example": "Bomba centrífuga"})
    mantenimiento_general_id: UUID4 = Field(..., json_schema_extra={"example": "123e4567-e89b-12d3-a456-426614174000"})
    reporte: Optional[Dict] = Field(None, json_schema_extra={"example": {"presion": "2.5 bar"}})

    model_config = ConfigDict(arbitrary_types_allowed=True)

class EquipoMantenimientoUpdate(BaseModel):
    equipo: Optional[str] = Field(None, min_length=3, max_length=50, json_schema_extra={"example": "Bomba actualizada"})
    mantenimiento_general_id: Optional[UUID4] = Field(None, json_schema_extra={"example": "123e4567-e89b-12d3-a456-426614174000"})
    reporte: Optional[Dict] = Field(None, json_schema_extra={"example": {"presion": "3.0 bar"}})

    model_config = ConfigDict(arbitrary_types_allowed=True)

class EquipoMantenimientoRead(BaseModel):
    id: UUID4
    equipo: str
    created_at: datetime
    mantenimiento_general_id: UUID4
    reporte: Optional[Dict] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

class EquipoMantenimientoResponse(BaseModel):
    id: UUID4
    equipo: str
    created_at: datetime
    mantenimiento_general_id: UUID4
    reporte: Optional[Dict] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)