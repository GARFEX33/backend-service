from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column
from uuid import UUID, uuid4
from datetime import datetime

if TYPE_CHECKING:
    from .foto_mantenimiento import FotoMantenimiento

class EquipoMantenimiento(SQLModel, table=True):
    __tablename__ = "equipomantenimiento"

    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    equipo: str
    created_at: datetime = Field(default_factory=datetime.now)
    mantenimiento_general_id: UUID = Field(foreign_key="mantenimientogeneral.id")
    reporte: Optional[dict] = Field(sa_column=Column(JSON), default=None)

    fotos: List["FotoMantenimiento"] = Relationship(back_populates="equipos_mantenimiento")

    model_config = {"arbitrary_types_allowed": True}