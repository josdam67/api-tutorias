
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TutorCurso(BaseModel):
    id_tutor_curso: Optional[str] = Field(
        default=None,
        description="MongoDB "
    ) 
    id_tutor: str = Field(
        description="id del Tutor"
    )
    id_curso: str = Field (
        description="id del Curso"
    )
    fecha_aprobacion: Optional[datetime]

class TutorCreate(BaseModel):
    id_tutor: str
    id_curso: str

    class Config:
        schema_extra = {
            "example": {
                "id_tutor": "64f2b2b86e8c4f77b3a2d3f3",
                "id_curso": "64f2b2a76e8c4f77b3a2d3f2"
            }
        }

class TutorCursoDB(TutorCurso):
    id_tutor_curso: str

    