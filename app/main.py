from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles

from app.core import error_handlers
from app.db.database import create_db_and_tables

from app.api.v1.endpoints.foto_mantenimiento import router as foto_mantenimiento_router
from app.api.v1.endpoints.equipo_mantenimiento import router as equipo_mantenimiento_router
from app.api.v1.endpoints.ubicacion import router as ubicacion_router
from app.api.v1.endpoints.mantenimiento_general import router as mantenimiento_general_router
from app.api.v1.endpoints.cliente import router as cliente_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Mantenimiento API",
    version="1.0.0",
    description="API para la gestión de mantenimiento de equipos y ubicaciones",
    lifespan=lifespan,
)

# Configurar StaticFiles para servir archivos de media
app.mount("/media", StaticFiles(directory="media"), name="media")

# Registrar handlers personalizados
app.add_exception_handler(HTTPException, error_handlers.http_exception_handler)
app.add_exception_handler(RequestValidationError, error_handlers.validation_exception_handler)
app.add_exception_handler(IntegrityError, error_handlers.integrity_error_handler)
app.add_exception_handler(Exception, error_handlers.general_exception_handler)

# Registro de routers
app.include_router(mantenimiento_general_router, prefix="/api/v1/mantenimiento_general", tags=["mantenimiento_general"])
app.include_router(foto_mantenimiento_router, prefix="/api/v1/foto_mantenimiento", tags=["foto_mantenimiento"])
app.include_router(equipo_mantenimiento_router, prefix="/api/v1/equipo_mantenimiento", tags=["equipo_mantenimiento"])
app.include_router(ubicacion_router, prefix="/api/v1/ubicacion", tags=["ubicacion"])
app.include_router(cliente_router, prefix="/api/v1/cliente", tags=["cliente"])
