from utils.mongo import get_collection
from bson import ObjectId

def crear_sesion(data):
    cursos_col = get_collection("cursos")    # ←
    usuarios_col = get_collection("usuarios")# ←
    sesiones_col = get_collection("sesiones")# ←

    if not cursos_col.find_one({"_id": ObjectId(data["id_curso"])}):
        raise Exception("El curso no existe")

    tutor = usuarios_col.find_one({"_id": ObjectId(data["id_tutor"]), "tipo_usuario": "Tutor"})
    if not tutor:
        raise Exception("El tutor no existe o no tiene el tipo correcto ")

    result = sesiones_col.insert_one(data)
    return {"id_sesion": str(result.inserted_id)}

def obtener_sesion(id_sesion):
    sesiones_col = get_collection("sesiones")  # ←
    sesion = sesiones_col.find_one({"_id": ObjectId(id_sesion)})
    if not sesion:
        return None
    return {**sesion, "id_sesion": str(sesion["_id"])}

def actualizar_sesion(id_sesion, data):
    sesiones_col = get_collection("sesiones")  # ←
    result = sesiones_col.update_one({"_id": ObjectId(id_sesion)}, {"$set": data})
    return result.modified_count > 0

def eliminar_sesion(id_sesion):
    sesiones_col = get_collection("sesiones")  # ←
    result = sesiones_col.delete_one({"_id": ObjectId(id_sesion)})
    return result.deleted_count > 0
