from fastapi import APIRouter, HTTPException
from controllers import inscripcion_controller
from models.inscripcion_model import InscripcionCreate,IncripcionDB
from typing import List


router = APIRouter(prefix= "/inscripciones", tags=["Inscripciones"])


@router.post("/" , response_model=IncripcionDB)
def crear_inscripcion(data: InscripcionCreate):
    try:
        return inscripcion_controller.crear_inscripcion(data.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/", response_model=List[IncripcionDB])
def listar_inscripciones():
    return inscripcion_controller.listar_inscripciones()


@router.get("/{id_inscripcion}", response_model=IncripcionDB)
def obtener_inscripcion(id_inscripcion: str):
    ins = inscripcion_controller.obtener_inscripcion(id_inscripcion)
    if not ins:
        raise HTTPException(status_code=404, detail="Inscripcion no encontrada")
    return ins

@router.put("/{id_inscripcion}",response_model=dict)
def actualizar_inscripcion(id_inscripcion: str, data: InscripcionCreate):
    actualizado = inscripcion_controller.actualizar_inscripcion(id_inscripcion, data.dict())
    if not actualizado:
        raise HTTPException(status_code=404, detail="No se pudo actualizar")
    return {"msg":"Inscripcion Actualizada"}


@router.delete("/{id_inscripcion}", response_model=dict)
def eliminar_inscripcion(id_inscripcion: str):
    eliminado = inscripcion_controller.eliminar_inscripcion(id_inscripcion)
    if not eliminado:
        raise HTTPException(status_code=404, detail="No se pudo eliminar")
    return {"msg": "Inscripción eliminada"}