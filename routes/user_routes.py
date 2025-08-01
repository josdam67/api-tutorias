from fastapi import APIRouter, HTTPException, Body
from controllers import user_controller
from models.user_model import UserCreate, FirebaseLogin,UserLogin


router = APIRouter(prefix="/users", tags=["Usuarios"])



@router.post("/")
def register(data: UserCreate):
    try:
        return user_controller.register_user(data.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

#Haremos un login para verificar 
@router.post("/loginn")
def login_datos(data: UserLogin):
    try:
        return user_controller.login_datos(data)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
#un login con el Firebase Token
@router.post("/login")
def login(payload: FirebaseLogin):
    try:
        return user_controller.login_user(payload.firebase_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    


