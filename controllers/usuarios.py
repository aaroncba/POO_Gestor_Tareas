import os
import logging
import requests
from pymongo.mongo_client import MongoClient
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth

from fastapi import HTTPException

from models.usuarios import Usuario
from utils.mongodb import get_collection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cred = credentials.Certificate("secrets/gestor.json")
firebase_admin.initialize_app(cred)


async def create_usuario(user: Usuario) -> Usuario: 
    user_record = {}

    try: 
        user_record = firebase_auth.create_user(
            email = user.email, 
            password = user.password
        )
    except Exception as e: 
        logger.warning(e)
        raise HTTPException(
            status_code=400, detail="Error registrando usuario en Firebase"
        )
    
    try: 
        coll = get_collection("usuarios")

        new_usuario = Usuario(
            nombre = user.nombre
            ,apellido= user.apellido
            ,email = user.email
            ,fecha_registro= user.fecha_registro
            ,active = user.active
            ,admin = user.admin
            ,password = user.password
        )

        user_dict = new_usuario.model_dump(exclude={"id", "password"})
        inserted = coll.insert_one(user_dict)
        new_usuario.id = str(inserted.inserted_id)
        new_usuario.password = "********"
        return new_usuario
    except Exception as e: 
        firebase_auth.delete_user(user_record.uid)        
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code = 500, detail = f"Database error: {str(e)}")

