import os
from fastapi import UploadFile
from sqlmodel import Session, select
from app.models.foto_mantenimiento import FotoMantenimiento
from app.schemas.foto_mantenimiento import FotoMantenimientoCreate, FotoMantenimientoUpdate
from uuid import UUID, uuid4
from typing import List, Optional

async def get_foto_mantenimientos(session: Session, skip: int = 0, limit: int = 100) -> List[FotoMantenimiento]:
    """Get a list of foto_mantenimientos with pagination."""
    return session.exec(select(FotoMantenimiento).offset(skip).limit(limit)).all()

async def get_foto_mantenimiento(session: Session, id: UUID) -> Optional[FotoMantenimiento]:
    """Get a single foto_mantenimiento by ID."""
    return session.get(FotoMantenimiento, id)

async def create_foto_mantenimiento(session: Session, foto_create: FotoMantenimientoCreate) -> FotoMantenimiento:
    """Create a new foto_mantenimiento."""
    db_foto = FotoMantenimiento.model_validate(foto_create.model_dump())
    session.add(db_foto)
    session.commit()
    session.refresh(db_foto)
    return db_foto

async def update_foto_mantenimiento(session: Session, id: UUID, foto_update: FotoMantenimientoUpdate) -> Optional[FotoMantenimiento]:
    """Update an existing foto_mantenimiento."""
    db_foto = await get_foto_mantenimiento(session, id)
    if not db_foto:
        return None

    update_data = foto_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_foto, key, value)

    session.add(db_foto)
    session.commit()
    session.refresh(db_foto)
    return db_foto



async def save_and_register_foto(
    session: Session,
    categoria: str,
    equipos_mantenimiento_id: UUID,
    file: UploadFile
) -> FotoMantenimiento:
    ext = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{ext}"

    directory = f"media/{categoria}"
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    public_url = f"/media/{categoria}/{filename}"

    foto_create = FotoMantenimientoCreate(
        categoria=categoria,
        url=public_url,
        nombre=filename,
        equipos_mantenimiento_id=equipos_mantenimiento_id
    )

    db_foto = FotoMantenimiento.model_validate(foto_create.model_dump())
    session.add(db_foto)
    session.commit()
    session.refresh(db_foto)
    return db_foto

async def delete_foto_mantenimiento(session: Session, id: UUID) -> FotoMantenimiento | None:
    """Elimina el registro de foto y borra el archivo físico si existe."""
    db_foto = session.get(FotoMantenimiento, id)
    if not db_foto:
        return None

    # Eliminar archivo físico
    file_path = db_foto.url.lstrip("/")  # elimina el "/" inicial de /media/...
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            # Log opcional: el archivo ya puede no existir o tener permisos
            pass

    # Eliminar de la base de datos
    session.delete(db_foto)
    session.commit()
    return db_foto