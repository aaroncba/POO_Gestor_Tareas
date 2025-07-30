from bson import ObjectId


def pipeline_get_tareas_por_usuario(usuario_id: str):
    """
    Retorna un pipeline para obtener tareas de un usuario específico
    con detalles de prioridad y estado.
    """
    return [
        {
            "$match": {
                "id_usuario": usuario_id
            }
        },
        {
            "$lookup": {
                "from": "estado",
                "localField": "estado",
                "foreignField": "_id",
                "as": "estado"
            }
        },
        {
            "$unwind": "$estado"
        },
        {
            "$lookup": {
                "from": "prioridad",
                "localField": "prioridad",
                "foreignField": "_id",
                "as": "prioridad"
            }
        },
        {
            "$unwind": "$prioridad"
        },
        {
            "$project": {
                "_id": 1,
                "nombre_tarea": 1,
                "descripcion": 1,
                "fecha_creacion": 1,
                "fecha_vencimiento": 1,
                "estado": "$estado.estado",
                "prioridad": "$prioridad.prioridad"
            }
        }
    ]


def pipeline_get_tarea_detalle(tarea_id: str):
    """
    Retorna un pipeline para obtener el detalle completo de una tarea específica
    por su ID, incluyendo usuario, prioridad y estado.
    """
    return [
        {
            "$match": {
                "_id": ObjectId(tarea_id)
            }
        },
        {
            "$lookup": {
                "from": "usuarios",
                "localField": "id_usuario",
                "foreignField": "_id",
                "as": "usuario"
            }
        },
        {
            "$unwind": "$usuario"
        },
        {
            "$lookup": {
                "from": "estado",
                "localField": "estado",
                "foreignField": "_id",
                "as": "estado"
            }
        },
        {
            "$unwind": "$estado"
        },
        {
            "$lookup": {
                "from": "prioridad",
                "localField": "prioridad",
                "foreignField": "_id",
                "as": "prioridad"
            }
        },
        {
            "$unwind": "$prioridad"
        },
        {
            "$project": {
                "_id": 1,
                "nombre_tarea": 1,
                "descripcion": 1,
                "fecha_creacion": 1,
                "fecha_vencimiento": 1,
                "estado": "$estado.estado",
                "prioridad": "$prioridad.prioridad",
                "usuario.email": 1,
                "usuario.nombre": 1,
                "usuario.apellido": 1
            }
        }
    ]
