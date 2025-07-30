from utils.mongo import db
from bson import ObjectId
from datetime import datetime

tutor_curso_col = db["tutor_curso"]
usuarios_col = db["usuarios"]
cursos_col = db["cursos"]

def agregar_tutor_a_curso(data):
    # Validar tutor
    tutor = usuarios_col.find_one({"_id": ObjectId(data.id_tutor), "tipo_usuario": "Tutor"})
    if not tutor:
        raise Exception("Tutor no válido")

    # Validar curso
    if not cursos_col.find_one({"_id": ObjectId(data.id_curso)}):
        raise Exception("Curso no existe")
    
    doc = data.dict()
    doc["fecha_aprobacion"] = datetime.utcnow()

    result = tutor_curso_col.insert_one(doc)

    return{
        "id_tutor_curso": str(result.inserted_id),
        **doc
    }

def listar_tutor_cursos():
    return [
        {
        
            "id_tutor_curso": str(tc["_id"]),
            "id_tutor": tc["id_tutor"],
            "id_curso": tc["id_curso"],
            "fecha_aprobacion": tc.get("fecha_aprobacion")
        
        }
        for tc in tutor_curso_col.find()
    ]

def eliminar_tutor_curso(id_tutor_curso):
    result = tutor_curso_col.delete_one({"_id": ObjectId(id_tutor_curso)})
    return result.deleted_count > 0
