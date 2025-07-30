from utils.mongo import db
from bson import ObjectId

def sesiones_con_detalle():
    pipeline = [
        {
            "$lookup": {
                "from": "cursos",
                "localField": "id_curso",
                "foreignField": "_id",
                "as": "curso"
            }
        },
        {
            "$lookup": {
                "from": "usuarios",
                "localField": "id_tutor",
                "foreignField": "_id",
                "as": "tutor"
            }
        },
        {
            "$unwind": "$curso"
        },
        {
            "$unwind": "$tutor"
        },
        {
            "$project": {
                "_id": 0,
                "id_sesion": {"$toString": "$_id"},
                "curso": "$curso.nombre_curso",
                "tutor": {"$concat": ["$tutor.nombre", " ", "$tutor.apellido"]},
                "fecha_hora_inicio": 1,
                "modalidad": 1,
                "estado_sesion": 1
            }
        }
    ]
    return list(db["sesiones"].aggregate(pipeline))

def total_inscripciones_por_curso():
    pipeline = [
        {
            "$lookup": {
                "from": "sesiones",
                "localField": "id_sesion",
                "foreignField": "_id",
                "as": "sesion"
            }
        },
        {"$unwind": "$sesion"},
        {
            "$group": {
                "_id": "$sesion.id_curso",
                "total_inscritos": {"$sum": 1}
            }
        },
        {
            "$lookup": {
                "from": "cursos",
                "localField": "_id",
                "foreignField": "_id",
                "as": "curso"
            }
        },
        {"$unwind": "$curso"},
        {
            "$project": {
                "curso": "$curso.nombre_curso",
                "total_inscritos": 1
            }
        }
    ]
    return list(db["inscripciones"].aggregate(pipeline))


def sesiones_llenas():
    pipeline = [
        {
            "$lookup": {
                "from": "inscripciones",
                "localField": "_id",
                "foreignField": "id_sesion",
                "as": "inscritos"
            }
        },
        {
            "$addFields": {
                "inscritos_count": {"$size": "$inscritos"}
            }
        },
        {
            "$match": {
                "$expr": {"$gte": ["$inscritos_count", "$capacidad_maxima_alumnos"]}
            }
        },
        {
            "$project": {
                "id_sesion": {"$toString": "$_id"},
                "capacidad_maxima_alumnos": 1,
                "inscritos_count": 1,
                "estado_sesion": 1
            }
        }
    ]
    return list(db["sesiones"].aggregate(pipeline))

