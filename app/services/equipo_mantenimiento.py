from sqlmodel import Session, select
from app.models.equipo_mantenimiento import EquipoMantenimiento
from app.schemas.equipo_mantenimiento import EquipoMantenimientoCreate, EquipoMantenimientoUpdate
from uuid import UUID
from typing import List, Optional

async def get_equipos_mantenimiento(session: Session, skip: int = 0, limit: int = 100) -> List[EquipoMantenimiento]:
    """Get a list of maintenance equipment with pagination."""
    return session.exec(select(EquipoMantenimiento).offset(skip).limit(limit)).all()

async def get_equipo_mantenimiento(session: Session, id: UUID) -> Optional[EquipoMantenimiento]:
    """Get a single maintenance equipment by ID."""
    return session.get(EquipoMantenimiento, id)

async def create_equipo_mantenimiento(session: Session, equipo_create: EquipoMantenimientoCreate) -> EquipoMantenimiento:
    """Create a new maintenance equipment."""
    db_equipo = EquipoMantenimiento.model_validate(equipo_create.model_dump())
    session.add(db_equipo)
    session.commit()
    session.refresh(db_equipo)
    return db_equipo

async def update_equipo_mantenimiento(session: Session, id: UUID, equipo_update: EquipoMantenimientoUpdate) -> Optional[EquipoMantenimiento]:
    """Update an existing maintenance equipment."""
    db_equipo = await get_equipo_mantenimiento(session, id)
    if not db_equipo:
        return None

    update_data = equipo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_equipo, key, value)

    session.add(db_equipo)
    session.commit()
    session.refresh(db_equipo)
    return db_equipo

async def delete_equipo_mantenimiento(session: Session, id: UUID) -> Optional[EquipoMantenimiento]:
    """Delete a maintenance equipment by ID."""
    db_equipo = await get_equipo_mantenimiento(session, id)
    if not db_equipo:
        return None

    session.delete(db_equipo)
    session.commit()
    return db_equipo