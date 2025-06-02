from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.schemas.equipo_mantenimiento import (
    EquipoMantenimientoCreate,
    EquipoMantenimientoUpdate,
    EquipoMantenimientoRead,
    EquipoMantenimientoResponse
)
from app.db.database import get_session
from app.services.equipo_mantenimiento import (
    get_equipos_mantenimiento,
    get_equipo_mantenimiento,
    create_equipo_mantenimiento,
    update_equipo_mantenimiento,
    delete_equipo_mantenimiento
)
from app.utils.response import response_success, response_error
from app.schemas.types import ResponseSuccess
from uuid import UUID
from typing import List
from sqlalchemy.exc import IntegrityError

router = APIRouter(tags=["equipo_mantenimiento"])

@router.post("/", response_model=ResponseSuccess[EquipoMantenimientoResponse], status_code=status.HTTP_201_CREATED)
async def create_equipo_mantenimiento_endpoint(equipo: EquipoMantenimientoCreate, session: Session = Depends(get_session)):
    try:
        db_equipo = await create_equipo_mantenimiento(session, equipo)
        return response_success(data=EquipoMantenimientoResponse.model_validate(db_equipo, from_attributes=True))
    except IntegrityError:
        return response_error(status_code=status.HTTP_409_CONFLICT, detail="Error de integridad: es posible que el equipo ya exista o haya datos conflictivos.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear equipo")

@router.get("/", response_model=ResponseSuccess[List[EquipoMantenimientoRead]], status_code=status.HTTP_200_OK, summary="Obtener lista de equipos de mantenimiento", description="Recupera una lista paginada de equipos de mantenimiento")
async def read_equipos_mantenimiento(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    try:
        resultados = await get_equipos_mantenimiento(session, skip, limit)
        equipos = [EquipoMantenimientoRead.model_validate(e, from_attributes=True) for e in resultados]
        return response_success(data=equipos)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener equipos")

@router.get("/{id}", response_model=ResponseSuccess[EquipoMantenimientoResponse], responses={404: {"description": "Equipo no encontrado"}}, summary="Obtener un equipo por ID", description="Recupera un equipo de mantenimiento específico por su ID")
async def read_equipo_mantenimiento_by_id(id: UUID, session: Session = Depends(get_session)):
    try:
        equipo = await get_equipo_mantenimiento(session, id)
        if not equipo:
            return response_error(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo de mantenimiento no encontrado")
        return response_success(data=EquipoMantenimientoResponse.model_validate(equipo, from_attributes=True))
    except Exception as e:
        raise e

@router.put("/{id}", response_model=ResponseSuccess[EquipoMantenimientoResponse], responses={400: {"description": "Datos inválidos"}, 404: {"description": "Equipo no encontrado"}, 409: {"description": "Ya existe otro equipo con este nombre"}})
async def update_equipo_mantenimiento_endpoint(id: UUID, equipo: EquipoMantenimientoUpdate, session: Session = Depends(get_session)):
    try:
        db_equipo = await update_equipo_mantenimiento(session, id, equipo)
        if not db_equipo:
            return response_error(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo de mantenimiento no encontrado")
        return response_success(data=EquipoMantenimientoResponse.model_validate(db_equipo, from_attributes=True))
    except IntegrityError:
        return response_error(status_code=status.HTTP_409_CONFLICT, detail="Error de integridad al actualizar equipo: posible nombre duplicado o datos conflictivos.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al actualizar equipo")

@router.delete("/{id}", response_model=ResponseSuccess[EquipoMantenimientoResponse], responses={404: {"description": "Equipo no encontrado"}, 500: {"description": "Error interno del servidor"}})
async def delete_equipo_mantenimiento_endpoint(id: UUID, session: Session = Depends(get_session)):
    try:
        equipo = await delete_equipo_mantenimiento(session, id)
        if not equipo:
            return response_error(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo de mantenimiento no encontrado")
        return response_success(data=EquipoMantenimientoResponse.model_validate(equipo, from_attributes=True))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar equipo")