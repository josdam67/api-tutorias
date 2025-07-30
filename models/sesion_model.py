from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Sesion(BaseModel):
    id_curso: str = Field(..., description="ID del curso")
    id_tutor: str = Field(..., description="ID del tutor (user tipo 'Tutor')")
    fecha_hora_inicio: datetime
    fecha_hora_fin: datetime
    capacidad_maxima_alumnos: int
    modalidad: str # tomando en cuenta la sugerencia de que sea online o bien presencial
    estado_sesion: str #Si ya esta programada, activa o termino
    url_sesion: Optional[str]


class SesionCreate(Sesion):
    pass

class SesionDB(Sesion):
    id_sesion: str

