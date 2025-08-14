from utils.mongo import get_collection
from bson import ObjectId
from datetime import datetime

def crear_inscripcion(data):
    sesiones_col = get_collection("sesiones")       # ←
    usuarios_col = get_collection("usuarios")       # ←
    inscripciones_col = get_collection("inscripciones")  # ←

    if not sesiones_col.find_one({"_id": ObjectId(data["id_sesion"])}):
        raise Exception("Sesion no encontrada")

    estudiante = usuarios_col.find_one({"_id": ObjectId(data["id_estudiante"]), "tipo_usuario": "Estudiante"})
    if not estudiante:
        raise Exception("Estudiante no valido")

    data["fecha_inscripcion"] = datetime.utcnow()
    result = inscripciones_col.insert_one(data)
    return {
        "id_inscripcion": str(result.inserted_id),
        "id_estudiante": data["id_estudiante"],
        "id_sesion": data["id_sesion"],
        "estado_inscripcion": data["estado_inscripcion"],
        "puntuacion": data.get("puntuacion"),
        "comentario_valoracion": data.get("comentario_valoracion"),
        "fecha_valoracion": data.get("fecha_valoracion"),
        "fecha_inscripcion": data["fecha_inscripcion"],
    }

def listar_inscripciones():
    inscripciones_col = get_collection("inscripciones")  # ←
    return [{**ins, "id_inscripcion": str(ins["_id"])} for ins in inscripciones_col.find()]

def obtener_inscripcion(id_inscripcion):
    inscripciones_col = get_collection("inscripciones")  # ←
    ins = inscripciones_col.find_one({"_id": ObjectId(id_inscripcion)})
    if not ins:
        return None
    return {**ins, "id_inscripcion": str(ins["_id"])}

def actualizar_inscripcion(id_inscripcion, data):
    inscripciones_col = get_collection("inscripciones")  # ←
    result = inscripciones_col.update_one({"_id": ObjectId(id_inscripcion)}, {"$set": data})
    return result.modified_count > 0

def eliminar_inscripcion(id_inscripcion):
    inscripciones_col = get_collection("inscripciones")  # ←
    result = inscripciones_col.delete_one({"_id": ObjectId(id_inscripcion)})
    return result.deleted_count > 0
