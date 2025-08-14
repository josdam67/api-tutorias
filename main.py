import logging

from fastapi import FastAPI, Request
from dotenv import load_dotenv
import uvicorn
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from utils.mongo import get_collection, test_connection

from controllers.user_controller import register_user
from models.user_model import UserBase, FirebaseLogin

from routes import (
    user_routes,
    curso_routes,
    sesion_routes,
    inscripcion_routes,
    tutor_curso_routes,
    pipeline_routes,
    sesion_public_routes
)

load_dotenv()

URI = os.getenv("MONGODB_URI")

app = FastAPI(
    title="API Tutorías",
    description="API RESTful para gestión de sesiones de tutoría entre tutores y estudiantes.",
    version="1.0.0"
)



# Registrar routes
app.include_router(user_routes.router)
app.include_router(curso_routes.router)
app.include_router(sesion_routes.router)
app.include_router(inscripcion_routes.router)
app.include_router(tutor_curso_routes.router)
app.include_router(pipeline_routes.router)
app.include_router(sesion_public_routes.router)

@app.get("/")
def read_root():
    return {"version": "0.0.0"}

@app.post("/users")
async def create_user_endpoint(user: UserBase) -> UserBase:
    return await register_user(user)

@app.post("/login")
async def login_access(l: FirebaseLogin) -> dict:
    return 1


@app.get("/health")
def health_check():
    try:
        return {
            "status": "helalthy",
            "timestamp": "2025-08-9",
            "service": "API Tutorías",
            "environment": "production"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }   
    
@app.get("/ready")
def readiness_check():
    try:
        from utils.mongo import test_connection
        db_status = test_connection()
        return {
            "status": "ready" if db_status else "not ready",
            "database": "conected" if db_status else "disconnected",
            "service": "API Tutorías",
        }
    except Exception as e:
        return {
            "status": "not ready",
            "error": str(e)
        }
    




#@app.get("/exampleadmin")
#@validateadmin
#async def example_admin(request: Request):
#    return {
#        "message": "This is an example admin endpoint."
#        , "admin": request.state.admin
#    }

#@app.get("/exampleuser")
#@validateuser
#async def example_user(request: Request):
#    return {
#        "message": "This is an example user endpoint."
#        ,"email": request.state.email
#    }


# Punto de entrada
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)