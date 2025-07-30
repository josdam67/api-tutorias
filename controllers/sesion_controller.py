from utils.mongo import db
from bson import ObjectId
from datetime import datetime


sesiones_col = db ["sesiones"]
usuarios_col = db ["usuarios"]
cursos_col = db ["cursos"]

def crear_sesion(data):
    #buscamos una validacion si curso existe
    if not cursos_col.find_one({"_id": ObjectId(data["id_curso"])}):
        raise Exception("El curso no existe")
    
    #una validacion si el tutor existe y que tipo de tutor es 
    tutor = usuarios_col.find_one({"_id": ObjectId(data["id_tutor"]),"tipo_usuario": "Tutor"})
    if not tutor:
        raise Exception("El tutor no existe o no tiene el tipo correcto ")
    
    #insertando una sesion
    result = sesiones_col.insert_one(data)
    return{"id_sesion" : str(result.inserted_id)}

def obtener_sesion(id_sesion):
    sesion = sesiones_col.find_one({"_id": ObjectId(id_sesion)})
    if not sesion:
        return None
    return{**sesion, "id_sesion": str(sesion["_id"])}

def actualizar_sesion(id_sesion, data):
    result = sesiones_col.update_one({"_id": ObjectId(id_sesion)}, {"$set": data})
    return result.modified_count > 0



def eliminar_sesion(id_sesion):
    result = sesiones_col.delete_one({"_id": ObjectId(id_sesion)})
    return result.deleted_count > 0
