from typing import Optional
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class MantenimientoGeneral(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    cliente_id: UUID = Field(foreign_key="cliente.id")
    ubicacion_id: UUID = Field(foreign_key="ubicacion.id")
    periodo: str
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = {"arbitrary_types_allowed": True}