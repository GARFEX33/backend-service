from sqlmodel import Session, select
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate
from uuid import UUID
from typing import List, Optional

async def get_clientes(session: Session, skip: int = 0, limit: int = 100) -> List[Cliente]:
    """Get a list of clients with pagination."""
    return session.exec(select(Cliente).offset(skip).limit(limit)).all()

async def get_cliente(session: Session, id: UUID) -> Optional[Cliente]:
    """Get a single client by ID."""
    return session.get(Cliente, id)

async def create_cliente(session: Session, cliente_create: ClienteCreate) -> Cliente:
    """Create a new client."""
    db_cliente = Cliente(nombre=cliente_create.nombre)
    session.add(db_cliente)
    session.commit()
    session.refresh(db_cliente)
    return db_cliente

async def update_cliente(session: Session, id: UUID, cliente_update: ClienteUpdate) -> Optional[Cliente]:
    """Update an existing client."""
    db_cliente = await get_cliente(session, id)
    if not db_cliente:
        return None

    update_data = cliente_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_cliente, key, value)

    session.add(db_cliente)
    session.commit()
    session.refresh(db_cliente)
    return db_cliente

async def delete_cliente(session: Session, id: UUID) -> Optional[Cliente]:
    """Delete a client by ID."""
    db_cliente = await get_cliente(session, id)
    if not db_cliente:
        return None

    session.delete(db_cliente)
    session.commit()
    return db_cliente