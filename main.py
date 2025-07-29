import os
from fastapi import FastAPI, HTTPException
import uvicorn
import logging

from models.usuarios import Usuario
from controllers.usuarios import create_usuario

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
    

@app.get("/usuario/{tarea}")
async def tarea(tarea): 
    return {"tarea ": tarea}

if __name__ == "__main__": 
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")