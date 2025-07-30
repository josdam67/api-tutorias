
from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class InscripcionBase(BaseModel):
    id_estudiante: str
    id_sesion: str
    estado_inscripcion: str = "Activa" #tambien si esta completada, cancelada
    puntuacion: Optional[int] = None #tomando en cuenta una valoracion de entre 1-5
    comentario_valoracion: Optional[str] = None
    fecha_valoracion: Optional[datetime] = None

class InscripcionCreate(InscripcionBase):
        id_estudiante: str
        id_sesion: str
        estado_inscripcion: str = "Activa"
        puntuacion: Optional[int] = None
        comentario_valoracion: Optional[str] = None
        fecha_valoracion: Optional[datetime] = None

        class Config:
            schema_extra = {
            "example": {
                "id_estudiante": "64f2b2b86e8c4f77b3a2d3f3",
                "id_sesion": "64f2b2a76e8c4f77b3a2d3f2",
                "estado_inscripcion": "Activa",
                "puntuacion": 4,
                "comentario_valoracion": "Muy buena sesión",
                "fecha_valoracion": "2024-07-01T10:00:00"
            }
        }

        

class IncripcionDB(InscripcionBase):
    id_inscripcion: str
    fecha_inscripcion: datetime