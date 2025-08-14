from utils.mongo import get_collection
from bson import ObjectId
from bson.errors import InvalidId

def crear_curso(data):
    cursos_col = get_collection("cursos")  # ← antes era global
    result = cursos_col.insert_one(data)
    return {"id_curso": str(result.inserted_id)}

def listar_cursos():
    cursos_col = get_collection("cursos")  # ←
    cursos = []
    for curso in cursos_col.find():
        curso["id_curso"] = str(curso["_id"])
        curso.pop("_id", None)
        cursos.append(curso)
    return cursos

def obtener_curso(id_curso):
    cursos_col = get_collection("cursos")  # ←
    try:
        curso = cursos_col.find_one({"_id": ObjectId(id_curso)})
        if not curso:
            return None
        curso["id_curso"] = str(curso["_id"])
        curso.pop("_id", None)
        return curso
    except InvalidId:
        raise ValueError("ID de curso invalido")

def actualizar_curso(id_curso, data):
    cursos_col = get_collection("cursos")  # ←
    result = cursos_col.update_one({"_id": ObjectId(id_curso)}, {"$set": data})
    return result.modified_count > 0

def eliminar_curso(id_curso):
    cursos_col = get_collection("cursos")  # ←
    result = cursos_col.delete_one({"_id": ObjectId(id_curso)})
    return result.deleted_count > 0
