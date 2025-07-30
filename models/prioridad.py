from pydantic import BaseModel, Field
from typing import Optional

class Prioridad(BaseModel):
    id: Optional[str] = Field(
        default=None,  
        description="ID de MongoDB"
                              )
    prioridad: str = Field(
        description="Nivel de prioridad"
        )
    
class CrearPrioridad(BaseModel): 
    prioridad: str = Field(
        description= "Estado de la prioridad"
    )


    