from models.tareas import CrearTarea, Tareas
from models.estado import Estado, CrearEstado
from models.prioridad import Prioridad, CrearPrioridad
from pipelines.tarea_pipelines import pipeline_get_tarea_detalle, pipeline_get_tareas_por_usuario

from utils.mongodb import get_collection
from bson import ObjectId
from datetime import datetime


tarea_collection = get_collection("tareas")
usuario_collection = get_collection("usuarios")
prioridad_collection = get_collection("prioridad")
estado_collection = get_collection("estado")


async def crear_tarea(tarea_info: CrearTarea, user_id: str) -> dict: 
    try: 
        user_exists = usuario_collection.find_one({"_id": ObjectId(user_id)})
        """Todo: Programar los pipelines para obtener las tareas que ya existen"""
        existing_tarea = list(tarea_collection.aggregate(pipeline_get_tareas_por_usuario(user_id)))
        if existing_tarea: 
            return{
                "success": True, 
                "Message": "Ya tienes una orden en progreso", 
                "data": existing_tarea[0]
            }
        
        tarea_dict = {
            "id_usuario": ObjectId(user_id),
            "nombre_tarea": tarea_info.nombre_tarea,
            "descripcion": tarea_info.descripcion,
            "fecha_creacion": datetime.utcnow(),
            "fecha_vencimiento": tarea_info.fecha_vencimiento,
            "estado_id": ObjectId(tarea_info.estado_id),
            "prioridad_id": ObjectId(tarea_info.prioridad_id)
        }
        result = tarea_collection.insert_one(tarea_dict)
# Retornar la tarea creada con formato similar al existente
        created_tarea = {
            "_id": str(result.inserted_id),
            "id_usuario": user_id,
            "nombre_tarea": tarea_dict["nombre_tarea"],
            "descripcion": tarea_dict["descripcion"],
            "fecha_creacion": tarea_dict["fecha_creacion"].isoformat(),
            "fecha_vencimiento": tarea_dict["fecha_vencimiento"],
            "estado_id": str(tarea_dict["estado_id"]),
            "prioridad_id": str(tarea_dict["prioridad_id"])
        }

        return {
            "success": True,
            "message": "Tarea creada exitosamente",
            "data": created_tarea
        }

        
        

    except Exception as e: 
        return{"sucess": False, "message": f"Error: {str(e)}", "data":None}