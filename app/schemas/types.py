from pydantic import BaseModel, EmailStr, PositiveInt, Field, constr, field_validator, model_validator
from typing import Generic, TypeVar, Optional
import re

# Reusable types
class NombreCliente(BaseModel):
    value: str = Field(..., min_length=1, max_length=100)

    @field_validator('value')
    def validate_nombre_cliente(cls, v):
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', v):
            raise ValueError('Nombre debe contener solo letras y espacios')
        return v

    @model_validator(mode='before')
    def check_if_all_fields_valid(cls, values):
        # Puedes agregar validaciones entre varios campos si es necesario
        return values

T = TypeVar("T")

class ResponseSuccess(BaseModel, Generic[T]):
    status: str
    data: Optional[T]
    message: str
