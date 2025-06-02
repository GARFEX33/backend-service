from sqlmodel import Session, select
from app.models.mantenimiento_general import MantenimientoGeneral
from app.schemas.mantenimiento_general import MantenimientoGeneralCreate, MantenimientoGeneralUpdate
from uuid import UUID
from typing import List, Optional
from sqlalchemy.exc import IntegrityError

async def get_mantenimiento_general(session: Session, skip: int = 0, limit: int = 100) -> List[MantenimientoGeneral]:
    """Get a list of mantenimiento general records with pagination."""
    return session.exec(select(MantenimientoGeneral).offset(skip).limit(limit)).all()

async def get_mantenimiento_general_by_id(session: Session, id: UUID) -> Optional[MantenimientoGeneral]:
    """Get a single mantenimiento general record by ID."""
    return session.get(MantenimientoGeneral, id)

async def create_mantenimiento_general(session: Session, mantenimiento_create: MantenimientoGeneralCreate) -> MantenimientoGeneral:
    """Create a new mantenimiento general record."""
    db_mantenimiento = MantenimientoGeneral(**mantenimiento_create.model_dump())
    session.add(db_mantenimiento)
    session.commit()
    session.refresh(db_mantenimiento)
    return db_mantenimiento

async def update_mantenimiento_general(session: Session, id: UUID, mantenimiento_update: MantenimientoGeneralUpdate) -> Optional[MantenimientoGeneral]:
    """Update an existing mantenimiento general record."""
    db_mantenimiento = await get_mantenimiento_general_by_id(session, id)
    if not db_mantenimiento:
        return None

    update_data = mantenimiento_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_mantenimiento, key, value)

    session.add(db_mantenimiento)
    session.commit()
    session.refresh(db_mantenimiento)
    return db_mantenimiento

async def delete_mantenimiento_general(session: Session, id: UUID) -> Optional[MantenimientoGeneral]:
    """Delete a mantenimiento general record by ID."""
    db_mantenimiento = await get_mantenimiento_general_by_id(session, id)
    if not db_mantenimiento:
        return None

    session.delete(db_mantenimiento)
    session.commit()
    return db_mantenimiento