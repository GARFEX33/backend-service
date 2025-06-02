from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.db.database import get_session
from uuid import UUID
from typing import List
from sqlalchemy.exc import IntegrityError

from app.schemas.mantenimiento_general import MantenimientoGeneralCreate, MantenimientoGeneralUpdate, MantenimientoGeneralRead
from app.services.mantenimiento_general import (
    get_mantenimiento_general,
    get_mantenimiento_general_by_id,
    create_mantenimiento_general,
    update_mantenimiento_general,
    delete_mantenimiento_general
)
from app.utils.response import response_success, response_error
from app.schemas.types import ResponseSuccess

router = APIRouter(tags=["mantenimiento_general"])

@router.get("/", response_model=ResponseSuccess[List[MantenimientoGeneralRead]], status_code=status.HTTP_200_OK, summary="Obtener lista de mantenimiento general", description="Recupera una lista paginada de registros de mantenimiento general")
async def read_mantenimiento_general(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    """
    Parámetros:
    - skip: Número de registros a omitir (default 0)
    - limit: Número máximo de registros a devolver (default 100)

    Devuelve:
    - Lista de registros de mantenimiento general con paginación
    """
    resultados = await get_mantenimiento_general(session, skip, limit)
    return response_success(data=[MantenimientoGeneralRead.model_validate(c, from_attributes=True) for c in resultados])

@router.get("/{id}", response_model=ResponseSuccess[MantenimientoGeneralRead], responses={404: {"description": "MantenimientoGeneral no encontrado"}}, summary="Obtener un registro de mantenimiento general por ID", description="Recupera un registro específico de mantenimiento general por su ID")
async def read_mantenimiento_general_by_id(id: UUID, session: Session = Depends(get_session)):
    mantenimiento = await get_mantenimiento_general_by_id(session, id)
    if not mantenimiento:
        return response_error(status_code=status.HTTP_404_NOT_FOUND, detail="MantenimientoGeneral no encontrado")
    return response_success(data=MantenimientoGeneralRead.model_validate(mantenimiento, from_attributes=True))

@router.post("/", response_model=ResponseSuccess[MantenimientoGeneralRead], status_code=status.HTTP_201_CREATED, responses={400: {"description": "Datos inválidos"}, 409: {"description": "Ya existe un registro con estos datos"}, 500: {"description": "Error interno del servidor"}})
async def create_mantenimiento_general_endpoint(mantenimiento: MantenimientoGeneralCreate, session: Session = Depends(get_session)):
    db_mantenimiento = await create_mantenimiento_general(session, mantenimiento)
    return response_success(data=MantenimientoGeneralRead.model_validate(db_mantenimiento, from_attributes=True))

@router.put("/{id}", response_model=ResponseSuccess[MantenimientoGeneralRead], responses={400: {"description": "Datos inválidos"}, 404: {"description": "MantenimientoGeneral no encontrado"}, 409: {"description": "Ya existe otro registro con estos datos"}})
async def update_mantenimiento_general_endpoint(id: UUID, mantenimiento: MantenimientoGeneralUpdate, session: Session = Depends(get_session)):
    db_mantenimiento = await update_mantenimiento_general(session, id, mantenimiento)
    if not db_mantenimiento:
        return response_error(status_code=status.HTTP_404_NOT_FOUND, detail="MantenimientoGeneral no encontrado")
    return response_success(data=MantenimientoGeneralRead.model_validate(db_mantenimiento, from_attributes=True))

@router.delete("/{id}", response_model=ResponseSuccess[MantenimientoGeneralRead], responses={404: {"description": "MantenimientoGeneral no encontrado"}, 409: {"description": "Conflicto al eliminar, registro referenciado"}, 500: {"description": "Error interno del servidor"}})
async def delete_mantenimiento_general_endpoint(id: UUID, session: Session = Depends(get_session)):
    mantenimiento = await delete_mantenimiento_general(session, id)
    if not mantenimiento:
        return response_error(status_code=status.HTTP_404_NOT_FOUND, detail="MantenimientoGeneral no encontrado")
    return response_success(data=MantenimientoGeneralRead.model_validate(mantenimiento, from_attributes=True))