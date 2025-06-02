from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import RequestValidationError

async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Error inesperado", "details": str(exc)},
    )

async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=409,
        content={"message": "Error de integridad", "details": str(exc.orig)},
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"message": "Error de validación", "details": exc.errors()},
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": "Error HTTP", "details": exc.detail},
    )
