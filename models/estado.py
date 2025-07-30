from pydantic import BaseModel, Field
from typing import Optional

class Estado(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id", description="ID de MongoDB")
    estado: str = Field(..., description="Estado de la tarea")

class CrearEstado(BaseModel): 
    estado: str = Field(
        description="Nombre del estado"
    )

    