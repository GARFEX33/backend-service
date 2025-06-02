from sqlmodel import Session, select
from app.models.ubicacion import Ubicacion
from app.schemas.ubicacion import UbicacionCreate, UbicacionUpdate
from uuid import UUID
from typing import List, Optional

async def get_ubicaciones(session: Session, skip: int = 0, limit: int = 100) -> List[Ubicacion]:
    """Get a list of locations with pagination."""
    return session.exec(select(Ubicacion).offset(skip).limit(limit)).all()

async def get_ubicacion(session: Session, id: UUID) -> Optional[Ubicacion]:
    """Get a single location by ID."""
    return session.get(Ubicacion, id)

async def create_ubicacion(session: Session, ubicacion_create: UbicacionCreate) -> Ubicacion:
    """Create a new location."""
    db_ubicacion = Ubicacion(**ubicacion_create.dict())
    session.add(db_ubicacion)
    session.commit()
    session.refresh(db_ubicacion)
    return db_ubicacion

async def update_ubicacion(session: Session, id: UUID, ubicacion_update: UbicacionUpdate) -> Optional[Ubicacion]:
    """Update an existing location."""
    db_ubicacion = await get_ubicacion(session, id)
    if not db_ubicacion:
        return None

    update_data = ubicacion_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_ubicacion, key, value)

    session.add(db_ubicacion)
    session.commit()
    session.refresh(db_ubicacion)
    return db_ubicacion

async def delete_ubicacion(session: Session, id: UUID) -> Optional[Ubicacion]:
    """Delete a location by ID."""
    db_ubicacion = await get_ubicacion(session, id)
    if not db_ubicacion:
        return None

    session.delete(db_ubicacion)
    session.commit()
    return db_ubicacion