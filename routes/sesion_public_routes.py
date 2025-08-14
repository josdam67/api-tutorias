from fastapi import APIRouter, Query
from utils.mongo import get_collection
from typing import Optional

router = APIRouter(prefix="/sesiones/public", tags=["Sesiones Públicas"])

@router.get("/")
def filtrar_sesiones(
    modalidad: Optional[str] = Query(None, description="Filtrar por modalidad: Online o Presencial"),
    estado_sesion: Optional[str] = Query(None, description="Filtrar por estado: Activa, Finalizada, etc."),
    capacidad_minima: Optional[int] = Query(None, description="Filtrar sesiones con que tenga almenos esta capacidad"),
):
    query = {}
    if modalidad:
        query["modalidad"] = modalidad
    if estado_sesion:
        query["estado_sesion"] = estado_sesion
    if capacidad_minima:
        query["capacidad_maxima_alumnos"] = {"$gte": capacidad_minima}

    sesiones_col = get_collection("sesiones")  # ←
    sesiones = sesiones_col.find(query)
    return [
        {
            "id_sesion": str(s["_id"]),
            "modalidad": s.get("modalidad"),
            "estado_sesion": s.get("estado_sesion"),
            "fecha_hora_inicio": s.get("fecha_hora_inicio"),
            "capacidad_maxima_alumnos": s.get("capacidad_maxima_alumnos"),
        }
        for s in sesiones
    ]

