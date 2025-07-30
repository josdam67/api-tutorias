from fastapi import APIRouter, HTTPException
from controllers import sesion_controller
from models.sesion_model import SesionCreate,SesionDB,Sesion
from bson import ObjectId
from typing import List


router = APIRouter(prefix="/sesiones", tags=["sesiones"])


@router.post("/", response_model=dict)
def crear_sesion(data: SesionCreate):
    try:
        return sesion_controller.crear_sesion(data.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


@router.get("/{id_sesion}", response_model=SesionDB)
def obtener_sesion(id_sesion: str):
    sesion = sesion_controller.obtener_sesion(id_sesion)
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesion no Encontrada")
    return sesion


@router.put("/{id_sesion}")
def actualizar_sesion(id_sesion: str, data: SesionCreate):
    actualizado = sesion_controller.actualizar_sesion(id_sesion, data.dict())
    if not actualizado:
        raise HTTPException(status_code=404,detail="No se puedo actualzar")
    return{"msg": " Sesion actualizada"}



@router.delete("/{id_sesion}")
def eliminar_sesion(id_sesion: str):
    eliminado = sesion_controller.eliminar_sesion(id_sesion)
    if not eliminado:
        raise HTTPException(status_code=404, detail="No se pudo Eliminar")
    return {"msg": "Sesion eliminada"}
