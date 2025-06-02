from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlmodel import Session
from app.models.foto_mantenimiento import FotoMantenimiento
from app.schemas.foto_mantenimiento import FotoMantenimientoCreate, FotoMantenimientoUpdate, FotoMantenimientoRead, FotoMantenimientoResponse, FotoUploadResponse
from app.db.database import get_session
from uuid import UUID
from typing import List

from app.services.foto_mantenimiento import get_foto_mantenimientos, get_foto_mantenimiento, create_foto_mantenimiento, save_and_register_foto, update_foto_mantenimiento, delete_foto_mantenimiento
from app.utils.response import response_success, response_error
from app.schemas.types import ResponseSuccess

router = APIRouter(tags=["foto_mantenimiento"])

@router.get("/", response_model=ResponseSuccess[List[FotoMantenimientoRead]], status_code=status.HTTP_200_OK, summary="Obtener lista de fotos de mantenimiento", description="Recupera una lista paginada de fotos de mantenimiento")
async def read_foto_mantenimientos(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    """
    Parámetros:
    - skip: Número de registros a omitir (default 0)
    - limit: Número máximo de registros a devolver (default 100)

    Devuelve:
    - Lista de fotos de mantenimiento con paginación
    """
    resultados = await get_foto_mantenimientos(session, skip, limit)
    return response_success(data=[FotoMantenimientoRead.model_validate(f, from_attributes=True) for f in resultados])

@router.get("/{id}", response_model=ResponseSuccess[FotoMantenimientoResponse], responses={404: {"description": "Foto de mantenimiento no encontrada"}}, summary="Obtener una foto de mantenimiento por ID", description="Recupera una foto de mantenimiento específica por su ID")
async def read_foto_mantenimiento_by_id(id: UUID, session: Session = Depends(get_session)):
    foto = await get_foto_mantenimiento(session, id)
    if not foto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Foto de mantenimiento no encontrada")
    return response_success(data=FotoMantenimientoResponse.model_validate(foto, from_attributes=True))

@router.put("/{id}", response_model=ResponseSuccess[FotoMantenimientoResponse], responses={400: {"description": "Datos inválidos"}, 404: {"description": "Foto de mantenimiento no encontrada"}, 409: {"description": "Ya existe otra foto de mantenimiento con este nombre"}})
async def update_foto_mantenimiento_endpoint(id: UUID, foto_update: FotoMantenimientoUpdate, session: Session = Depends(get_session)):
    db_foto = await update_foto_mantenimiento(session, id, foto_update)
    if not db_foto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Foto de mantenimiento no encontrada")
    return response_success(data=FotoMantenimientoResponse.model_validate(db_foto, from_attributes=True))

@router.delete("/{id}", response_model=ResponseSuccess[FotoMantenimientoResponse], responses={404: {"description": "Foto de mantenimiento no encontrada"}, 409: {"description": "Conflicto al eliminar, foto referenciada"}, 500: {"description": "Error interno del servidor"}})
async def delete_foto_mantenimiento_endpoint(id: UUID, session: Session = Depends(get_session)):
    foto = await delete_foto_mantenimiento(session, id)
    if not foto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Foto de mantenimiento no encontrada")
    return response_success(data=FotoMantenimientoResponse.model_validate(foto, from_attributes=True))

@router.post("/upload", response_model=ResponseSuccess[FotoUploadResponse], status_code=status.HTTP_201_CREATED)
async def upload_foto_mantenimiento(
    categoria: str = Form(...),
    equipos_mantenimiento_id: UUID = Form(...),
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    try:
        db_foto = await save_and_register_foto(session, categoria, equipos_mantenimiento_id, file)
        return response_success(data=FotoUploadResponse.model_validate(db_foto, from_attributes=True))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al guardar archivo y registrar foto")