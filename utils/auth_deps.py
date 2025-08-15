
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.jwt_handler import decode_access_token

bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user(token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if token is None:
        raise HTTPException(status_code=401, detail="Falta Authorization Bearer token")
    payload = decode_access_token(token.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    # payload tiene: id_usuario, email, tipo_usuario
    return payload

def require_role(*allowed_roles):
    def _dep(user=Depends(get_current_user)):
        if user.get("tipo_usuario") not in allowed_roles:
            raise HTTPException(status_code=403, detail="No tienes permisos para esta acción")
        return user
    return _dep
