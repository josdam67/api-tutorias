from pydantic import BaseModel
from typing import Optional

class CursoBase(BaseModel):
    nombre_curso: str
    descripcion: Optional[str] =  None
    activo: bool = True


class CursoDB(CursoBase):
    id_curso: str