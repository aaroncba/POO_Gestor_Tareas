from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class Tareas(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="MongoDB ID - se genera automáticamente"
    )
    id_usuario: str = Field(
        description="ID del usuario que creó esta tarea"
    )
    nombre_tarea: str = Field(
        description="Nombre de la tarea"
    )
    descripcion: str = Field(
        description="Descripción de la tarea"
    )
    fecha_creacion: datetime = Field(
        default_factory=datetime.utcnow,
        description="Fecha cuando se creó la tarea"
    )
    fecha_vencimiento: datetime = Field(
        description="Fecha de vencimiento de la tarea"
    )
    prioridad_id: str = Field(
        description="ID de la prioridad de la tarea"
    )

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class crear_tarea(BaseModel):
    id_usuario: str = Field(
        description="ID del usuario que creó esta tarea"
    )
    nombre_tarea: str = Field(
        description="Nombre de la tarea"
    )
    descripcion: str = Field(
        description="Descripción de la tarea"
    )
    fecha_vencimiento: datetime = Field(
        description="Fecha de vencimiento de la tarea"
    )
    prioridad_id: str = Field(
        description="ID de la prioridad de la tarea"
    )

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }