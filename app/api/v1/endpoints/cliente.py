from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteRead
from app.db.database import get_session
from uuid import UUID
from typing import List
from sqlalchemy.exc import IntegrityError

from app.schemas.types import ResponseSuccess
from app.services.cliente import get_clientes, get_cliente, create_cliente, update_cliente, delete_cliente
from app.utils.response import response_success, response_error

router = APIRouter(tags=["cliente"])

@router.get("/", response_model=ResponseSuccess[List[ClienteRead]], status_code=status.HTTP_200_OK, summary="Obtener lista de clientes", description="Recupera una lista paginada de clientes")
async def read_clientes(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    """
    Parámetros:
    - skip: Número de registros a omitir (default 0)
    - limit: Número máximo de registros a devolver (default 100)

    Devuelve:
    - Lista de clientes con paginación
    """
    try:
        resultados = await get_clientes(session, skip, limit)
        clientes = [ClienteRead.model_validate(c, from_attributes=True) for c in resultados]
        return response_success(data=clientes)
    except Exception as e:
         raise e

@router.get("/{id}", response_model=ResponseSuccess[ClienteRead], responses={404: {"description": "Cliente no encontrado"}}, summary="Obtener un cliente por ID", description="Recupera un cliente específico por su ID")
async def read_cliente_by_id(id: UUID, session: Session = Depends(get_session)):
    try:
        cliente = await get_cliente(session, id)
        if not cliente:
            return response_error(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
        return response_success(data=cliente)
    except Exception as e:
        raise e

@router.post("/", response_model=ResponseSuccess[ClienteRead], status_code=status.HTTP_201_CREATED, responses={400: {"description": "Datos inválidos"}, 409: {"description": "Ya existe un cliente con este nombre"}, 500: {"description": "Error interno del servidor"}})
async def create_cliente_endpoint(cliente_create: ClienteCreate, session: Session = Depends(get_session)):
    try:
        db_cliente = await create_cliente(session, cliente_create)
        return response_success(data=ClienteRead.model_validate(db_cliente, from_attributes=True))  # Aseguramos la conversión

    except IntegrityError:
        return response_error(status_code=status.HTTP_409_CONFLICT, message="Error de integridad: es posible que el cliente ya exista o haya datos conflictivos.")
    except Exception as e:
        raise e


@router.put("/{id}", response_model=ResponseSuccess[ClienteRead], responses={400: {"description": "Datos inválidos"}, 404: {"description": "Cliente no encontrado"}, 409: {"description": "Ya existe otro cliente con este nombre"}})
async def update_cliente_endpoint(id: UUID, cliente_update: ClienteUpdate, session: Session = Depends(get_session)):
    try:
        db_cliente = await update_cliente(session, id, cliente_update)
        if not db_cliente:
            return response_error(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
        return response_success(data=db_cliente)
    except IntegrityError:
        return response_error(status_code=status.HTTP_409_CONFLICT, detail="Error de integridad al actualizar cliente: posible nombre duplicado o datos conflictivos.")
    except Exception as e:
        raise e

@router.delete("/{id}", response_model=ResponseSuccess[ClienteRead], responses={404: {"description": "Cliente no encontrado"}, 409: {"description": "Conflicto al eliminar, cliente referenciado"}, 500: {"description": "Error interno del servidor"}})
async def delete_cliente_endpoint(id: UUID, session: Session = Depends(get_session)):
    try:
        cliente = await delete_cliente(session, id)
        if not cliente:
            return response_error(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
        return response_success(data=cliente)
    except IntegrityError:
        return response_error(status_code=status.HTTP_409_CONFLICT, detail="No se puede eliminar el cliente. Puede estar referenciado por otros datos.")
    except Exception as e:
       raise e