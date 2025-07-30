from fastapi import APIRouter, HTTPException
from controllers import curso_controller
from models.curso_model import CursoBase,CursoDB
from typing import List
from pydantic import BaseModel



router = APIRouter(prefix="/cursos", tags=["Cursos"])

@router.post("/", response_model=dict)
def crear_curso(data: CursoBase):
    return curso_controller.crear_curso(data.dict())

@router.get("/", response_model=List[dict])
def listar_cursos():
    try:
        return curso_controller.listar_cursos()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{id_curso}")
def obtener_curso(id_curso: str):
    try:
        curso = curso_controller.obtener_curso(id_curso)
        if not curso:
            raise HTTPException(status_code=404, detail="Curso no encontrado")
        return curso
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    


@router.put("/{id_curso}")
def actualizar_curso(id_curso: str, data: CursoBase):
    actualizado = curso_controller.actualizar_curso(id_curso, data.dict())
    if not actualizado:
        raise HTTPException(status_code=404, detail="No se pudo actualizar")
    return {"msg": "Curso actualizado"}



@router.delete("/{id_curso}")
def eliminar_curso(id_curso: str):
    eliminado = curso_controller.eliminar_curso(id_curso)
    if not eliminado:
        raise HTTPException(status_code=404, detail="No se pudo eliminar")
    return {"msg": "Curso eliminado"}
