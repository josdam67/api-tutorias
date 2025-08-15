from fastapi import APIRouter, HTTPException, Body, Response
from controllers import user_controller
from models.user_model import UserCreate, FirebaseLogin, UserLogin

router = APIRouter(prefix="/users", tags=["Usuarios"])

# --- OPTIONS handlers para preflight CORS (con y sin slash) ---
@router.options("", include_in_schema=False)    # /users
def options_users_no_slash():
    return Response(status_code=200)

@router.options("/", include_in_schema=False)   # /users/
def options_users_slash():
    return Response(status_code=200)

@router.options("/loginn", include_in_schema=False)
def options_loginn():
    return Response(status_code=200)

@router.options("/login", include_in_schema=False)
def options_login():
    return Response(status_code=200)
# ---------------------------------------------------------------

# Signup (con y sin slash)
@router.post("")   # /users
def register_no_slash(data: UserCreate):
    try:
        return user_controller.register_user(data.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/")  # /users/
def register_slash(data: UserCreate):
    try:
        return user_controller.register_user(data.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Login email/password
@router.post("/loginn")
def login_datos(data: UserLogin):
    try:
        return user_controller.login_datos(data)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

# Login con firebase_token
@router.post("/login")
def login(payload: FirebaseLogin):
    try:
        return user_controller.login_user(payload.firebase_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
