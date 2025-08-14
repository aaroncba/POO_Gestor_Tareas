from models.prioridad import CrearPrioridad, Prioridad
from utils.mongodb import get_collection
from bson import ObjectId
from typing import List

# Obtener la colección de prioridades
prioridad_collection = get_collection("prioridad")

async def crear_prioridad(prioridad_info: CrearPrioridad) -> dict:
    try:
        # Verificar si ya existe una prioridad con el mismo nombre
        existing_prioridad = prioridad_collection.find_one({"prioridad": prioridad_info.prioridad})
        if existing_prioridad:
            return {
                "success": False,
                "message": f"Ya existe una prioridad con el nombre '{prioridad_info.prioridad}'",
                "data": None
            }

        # Crear el diccionario de la prioridad
        prioridad_dict = {
            "prioridad": prioridad_info.prioridad
        }

        # Insertar la prioridad en la colección
        result = prioridad_collection.insert_one(prioridad_dict)

        # Crear el objeto de respuesta
        created_prioridad = {
            "_id": str(result.inserted_id),
            "prioridad": prioridad_dict["prioridad"]
        }

        return {
            "success": True,
            "message": "Prioridad creada exitosamente",
            "data": created_prioridad
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "data": None
        }

async def obtener_prioridades() -> dict:
    print("Entro por aqui!!!!!!")
    try:
        # Obtener todas las prioridades de la colección
        prioridades = list(prioridad_collection.find())

        # Convertir los documentos a un formato compatible con el modelo Prioridad
        prioridades_list = [
            {
                "_id": str(prioridad["_id"]),
                "prioridad": prioridad["prioridad"]
            }
            for prioridad in prioridades
        ]

        return {
            "success": True,
            "message": "Prioridades obtenidas exitosamente",
            "data": prioridades_list
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}",
            "data": None
        }