# pipelines/sesion_pipelines.py
from utils.mongo import get_collection

def sesiones_con_detalle():
    sesiones_col = get_collection("sesiones")
    pipeline = [
        # Convierte strings a ObjectId para que el $lookup haga match con _id
        {"$addFields": {
            "id_curso_obj": {"$toObjectId": "$id_curso"},
            "id_tutor_obj": {"$toObjectId": "$id_tutor"},
        }},
        {
            "$lookup": {
                "from": "cursos",
                "localField": "id_curso_obj",
                "foreignField": "_id",
                "as": "curso"
            }
        },
        {
            "$lookup": {
                "from": "usuarios",
                "localField": "id_tutor_obj",
                "foreignField": "_id",
                "as": "tutor"
            }
        },
        {"$unwind": "$curso"},
        {"$unwind": "$tutor"},
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
    return list(sesiones_col.aggregate(pipeline))

def total_inscripciones_por_curso():
    inscripciones_col = get_collection("inscripciones")
    pipeline = [
        # Convierte string id_sesion a ObjectId para unir con sesiones._id
        {"$addFields": {"id_sesion_obj": {"$toObjectId": "$id_sesion"}}},
        {
            "$lookup": {
                "from": "sesiones",
                "localField": "id_sesion_obj",
                "foreignField": "_id",
                "as": "sesion"
            }
        },
        {"$unwind": "$sesion"},
        # Ahora sesion.id_curso probablemente es string → conviértelo a ObjectId para unir con cursos._id
        {"$addFields": {"id_curso_obj": {"$toObjectId": "$sesion.id_curso"}}},
        {
            "$group": {
                "_id": "$id_curso_obj",
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
                "_id": 0,
                "curso": "$curso.nombre_curso",
                "total_inscritos": 1
            }
        }
    ]
    return list(inscripciones_col.aggregate(pipeline))

def sesiones_llenas():
    sesiones_col = get_collection("sesiones")
    pipeline = [
        # Une sesiones con inscripciones: inscripciones.id_sesion (string) → convertir para comparar con sesiones._id
        {"$lookup": {
            "from": "inscripciones",
            "let": {"ses_id": {"$toString": "$_id"}},  # convierte _id a string para comparar con id_sesion (string)
            "pipeline": [
                {"$match": {"$expr": {"$eq": ["$id_sesion", "$$ses_id"]}}}
            ],
            "as": "inscritos"
        }},
        {"$addFields": {"inscritos_count": {"$size": "$inscritos"}}},
        {"$match": {"$expr": {"$gte": ["$inscritos_count", "$capacidad_maxima_alumnos"]}}},
        {
            "$project": {
                "_id": 0,
                "id_sesion": {"$toString": "$_id"},
                "capacidad_maxima_alumnos": 1,
                "inscritos_count": 1,
                "estado_sesion": 1
            }
        }
    ]
    return list(sesiones_col.aggregate(pipeline))


