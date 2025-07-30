from fastapi import Header, HTTPException, status
from utils.jwt_handler import decode_access_token

def get_current_user(authorization: str = Header(...)):
    token = authorization.split(" ")[1] if " " in authorization else authorization
    user_data = decode_access_token(token)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    return user_data
