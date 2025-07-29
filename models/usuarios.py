from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Usuario(BaseModel): 
    id: Optional[str] = Field(
        default=None, 
        description="MongoDB Id - generado automaticamente"
    )
    nombre: str = Field(
        pattern= r"^[A-Za-z]+(?:[ '-][A-Za-z]+)*$", 
        description ="Primer Nombre del usuario"
    )
    apellido: str = Field(
        pattern= r"^[A-Za-z]+(?:[ '-][A-Za-z]+)*$", 
        description = "Apellido del usuario"
    )
    email: str = Field(
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        description = "Email del usuario"
    )
    fecha_registro: str = Field(
        pattern = r"^\d{4}-\d{2}-\d{2}$", 
        description= "Fecha de inscripcion del usuario"
    )
    active: bool = Field(
        default = True, 
        description= "Estado de la cuenta del usuario"
    )
    admin: bool = Field(
        default = False, 
        description="Definir si el usuario es administrador"
    )
    password: str = Field(
        min_length = 8, 
        max_length = 64, 
        description= "Contra del usuario, debe tener mas de 8 chars y menos 64 chars"
    ) 


@field_validator('password')
@classmethod
def validate_password_complexity(cls, value: str):
    if not re.search(r"[A-Z]", value):
        raise ValueError("La contraseña debe contener al menos una letra mayúscula.")
    if not re.search(r"\d", value):
        raise ValueError("La contraseña debe contener al menos un número.")
    if not re.search(r"[@$!%*?&]", value):
        raise ValueError("La contraseña debe contener al menos un carácter especial (@$!%*?&).")
    return value