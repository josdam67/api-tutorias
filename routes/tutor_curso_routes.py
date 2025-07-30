from fastapi import APIRouter, HTTPException, status
from controllers import tutor_curso_controller
from models.tutor_curso_model import TutorCreate,TutorCursoDB
from typing import List

router = APIRouter(prefix="/tutor_curso", tags=["TutorCurso"])

@router.post("/", response_model=TutorCursoDB, status_code=status.HTTP_201_CREATED)
def agregar_tutor(data: TutorCreate):
    try:
        return tutor_curso_controller.agregar_tutor_a_curso(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[TutorCursoDB])
def listar_tutor_cursos():
    return tutor_curso_controller.listar_tutor_cursos()

@router.delete("/{id_tutor_curso}")
def eliminar_tutor_curso(id_tutor_curso: str):
    eliminado = tutor_curso_controller.eliminar_tutor_curso(id_tutor_curso)
    if not eliminado:
        raise HTTPException(status_code=404, detail="No se pudo eliminar")
    return {"msg": "Relación tutor-curso eliminada"}
