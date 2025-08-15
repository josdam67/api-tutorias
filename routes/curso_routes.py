from fastapi import APIRouter, HTTPException, Depends
from controllers import curso_controller
from models.curso_model import CursoBase
from typing import List
from utils.auth_deps import require_role, get_current_user

router = APIRouter(prefix="/cursos", tags=["Cursos"])

# Listar cursos (público o autenticado; como prefieras)
@router.get("/", response_model=List[dict])
def listar_cursos(user=Depends(get_current_user)):  # ← si quieres hacerlo público, elimina el Depends
    try:
        return curso_controller.listar_cursos()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Obtener curso por id (opcionalmente público)
@router.get("/{id_curso}")
def obtener_curso(id_curso: str, user=Depends(get_current_user)):
    try:
        curso = curso_controller.obtener_curso(id_curso)
        if not curso:
            raise HTTPException(status_code=404, detail="Curso no encontrado")
        return curso
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# Crear curso → SOLO Admin
@router.post("/", response_model=dict, dependencies=[Depends(require_role("Admin"))])
def crear_curso(data: CursoBase):
    return curso_controller.crear_curso(data.dict())

# Actualizar curso → SOLO Admin
@router.put("/{id_curso}", dependencies=[Depends(require_role("Admin"))])
def actualizar_curso(id_curso: str, data: CursoBase):
    actualizado = curso_controller.actualizar_curso(id_curso, data.dict())
    if not actualizado:
        raise HTTPException(status_code=404, detail="No se pudo actualizar")
    return {"msg": "Curso actualizado"}

# Eliminar curso → SOLO Admin
@router.delete("/{id_curso}", dependencies=[Depends(require_role("Admin"))])
def eliminar_curso(id_curso: str):
    eliminado = curso_controller.eliminar_curso(id_curso)
    if not eliminado:
        raise HTTPException(status_code=404, detail="No se pudo eliminar")
    return {"msg": "Curso eliminado"}

