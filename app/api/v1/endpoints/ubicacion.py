from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.models.ubicacion import Ubicacion
from app.schemas.ubicacion import UbicacionCreate, UbicacionUpdate, UbicacionRead
from app.db.database import get_session
from uuid import UUID
from typing import List
from sqlalchemy.exc import IntegrityError

from app.services.ubicacion import (
    get_ubicaciones,
    get_ubicacion,
    create_ubicacion,
    update_ubicacion,
    delete_ubicacion
)
from app.utils.response import response_success, response_error
from app.schemas.types import ResponseSuccess

router = APIRouter(tags=["ubicacion"])

@router.get(
    "/",
    response_model=ResponseSuccess[List[UbicacionRead]],
    status_code=status.HTTP_200_OK,
    summary="Obtener lista de ubicaciones",
    description="Recupera una lista paginada de ubicaciones"
)
async def read_ubicaciones(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    try:
        resultados = await get_ubicaciones(session, skip, limit)
        ubicaciones = [UbicacionRead.model_validate(u, from_attributes=True) for u in resultados]
        return response_success(data=ubicaciones)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al obtener ubicaciones")

@router.get(
    "/{id}",
    response_model=ResponseSuccess[UbicacionRead],
    responses={404: {"description": "Ubicación no encontrada"}},
    summary="Obtener una ubicación por ID",
    description="Recupera una ubicación específica por su ID"
)
async def read_ubicacion_by_id(id: UUID, session: Session = Depends(get_session)):
    try:
        ubicacion = await get_ubicacion(session, id)
        if not ubicacion:
            return response_error(status_code=status.HTTP_404_NOT_FOUND, detail="Ubicación no encontrada")
        return response_success(data=UbicacionRead.model_validate(ubicacion, from_attributes=True))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al obtener ubicación")

@router.post(
    "/",
    response_model=ResponseSuccess[UbicacionRead],
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"description": "Datos inválidos"},
        409: {"description": "Ya existe una ubicación con este nombre"},
        500: {"description": "Error interno del servidor"}
    },
    summary="Crear una nueva ubicación",
    description="Crea una nueva ubicación con los datos proporcionados"
)
async def create_ubicacion_endpoint(
    ubicacion_create: UbicacionCreate,
    session: Session = Depends(get_session)
):
    try:
        db_ubicacion = await create_ubicacion(session, ubicacion_create)
        return response_success(data=UbicacionRead.model_validate(db_ubicacion, from_attributes=True))
    except IntegrityError:
        return response_error(status_code=status.HTTP_409_CONFLICT, message="Error de integridad: es posible que la ubicación ya exista o haya datos conflictivos.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor al crear ubicación")

@router.put(
    "/{id}",
    response_model=ResponseSuccess[UbicacionRead],
    responses={
        400: {"description": "Datos inválidos"},
        404: {"description": "Ubicación no encontrada"},
        409: {"description": "Ya existe otra ubicación con este nombre"}
    },
    summary="Actualizar una ubicación",
    description="Actualiza una ubicación existente con los datos proporcionados"
)
async def update_ubicacion_endpoint(
    id: UUID,
    ubicacion_update: UbicacionUpdate,
    session: Session = Depends(get_session)
):
    try:
        db_ubicacion = await update_ubicacion(session, id, ubicacion_update)
        if not db_ubicacion:
            return response_error(status_code=status.HTTP_404_NOT_FOUND, detail="Ubicación no encontrada")
        return response_success(data=UbicacionRead.model_validate(db_ubicacion, from_attributes=True))
    except IntegrityError:
        return response_error(status_code=status.HTTP_409_CONFLICT, detail="Error de integridad al actualizar ubicación: posible nombre duplicado o datos conflictivos.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor al actualizar ubicación")

@router.delete(
    "/{id}",
    response_model=ResponseSuccess[UbicacionRead],
    responses={
        404: {"description": "Ubicación no encontrada"},
        409: {"description": "Conflicto al eliminar, ubicación referenciada"},
        500: {"description": "Error interno del servidor"}
    },
    summary="Eliminar una ubicación",
    description="Elimina una ubicación por su ID"
)
async def delete_ubicacion_endpoint(id: UUID, session: Session = Depends(get_session)):
    try:
        ubicacion = await delete_ubicacion(session, id)
        if not ubicacion:
            return response_error(status_code=status.HTTP_404_NOT_FOUND, detail="Ubicación no encontrada")
        return response_success(data=UbicacionRead.model_validate(ubicacion, from_attributes=True))
    except IntegrityError:
        return response_error(status_code=status.HTTP_409_CONFLICT, detail="No se puede eliminar la ubicación. Puede estar referenciada por otros datos.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno del servidor al eliminar ubicación")