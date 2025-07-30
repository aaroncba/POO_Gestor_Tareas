import os
from fastapi import FastAPI, HTTPException, Request, APIRouter
import uvicorn
import logging

from models.usuarios import Usuario
from models.login import Login
from models.tareas import CrearTarea
from controllers.tareas import crear_tarea
from controllers.usuarios import create_usuario, login
from utils.security import validateuser





app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    return {"version": "0.0.0"}

@app.post("/usuarios/")
async def creacionUsuario(usuario : Usuario ) -> Usuario:
    try:
        return await create_usuario(usuario)
    except Exception as e: 
        raise HTTPException(status_code = 500, detail=str(e))
    finally: 
        logger.info("Intento de creacion de usuario")
    

@app.post("/login")
async def login_access(l: Login) -> dict:
    return login(l)


@app.get("/exampleuser")
@validateuser
async def example_user(request: Request):
    return {
        "message": "This is an example user endpoint."
        ,"email": request.state.email
    }


    
router = APIRouter()

@router.post("/tareas")
@validateuser
async def crear_tarea_endpoint(tarea: CrearTarea, request: Request):
    return await crear_tarea(tarea, request.state.user_id)
app.include_router(router)



if __name__ == "__main__": 
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")