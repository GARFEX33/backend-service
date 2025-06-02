from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from .equipo_mantenimiento import EquipoMantenimiento

class FotoMantenimiento(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    categoria: str
    url: str
    nombre: str
    equipos_mantenimiento_id: UUID = Field(foreign_key="equipomantenimiento.id")

    equipos_mantenimiento: Optional["EquipoMantenimiento"] = Relationship(back_populates="fotos")

    model_config = {"arbitrary_types_allowed": True}

