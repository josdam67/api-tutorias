from fastapi import APIRouter
from pipelines import sesion_pipelines

router = APIRouter(prefix="/pipelines", tags=["Pipelines"])

@router.get("/sesiones-detalle")
def get_sesiones_con_lookup():
    return sesion_pipelines.sesiones_con_detalle()

@router.get("/inscripciones-por-curso")
def get_inscripciones_por_curso():
    return sesion_pipelines.total_inscripciones_por_curso()

@router.get("/sesiones-llenas")
def get_sesiones_llenas():
    return sesion_pipelines.sesiones_llenas()
