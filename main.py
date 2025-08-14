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
from models.prioridad import CrearPrioridad, Prioridad
from controllers.prioridad import crear_prioridad, obtener_prioridades


from utils.security import verify_bearer_token



app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
@validateuser
async def root():
    return {"version": "0.0.0"}

@app.post("/usuarios/")
@validateuser
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


@app.post("/prioridades")
@validateuser
async def crear_prioridad_endpoint(prioridad: CrearPrioridad):
    return await crear_prioridad(prioridad)

@app.get("/prioridades")
@validateuser
async def obtener_prioridades_endpoint():
    return await obtener_prioridades()


"""Remove later :)"""
@app.get("/auth/check-token")
async def check_token(request: Request):
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(status_code=400, detail="Authorization header missing")

    try:
        scheme, token = authorization.split()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Authorization header format")

    if scheme.lower() != "bearer":
        raise HTTPException(status_code=400, detail="Invalid auth scheme")

    payload = verify_bearer_token(token)
    return {
        "success": True,
        "message": "Token is valid",
        "data": payload
    }


if __name__ == "__main__": 
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")