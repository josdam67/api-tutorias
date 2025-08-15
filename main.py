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
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response

load_dotenv()

URI = os.getenv("MONGODB_URI")

app = FastAPI(
    title="API Tutorías",
    description="API RESTful para gestión de sesiones de tutoría entre tutores y estudiantes.",
    version="1.0.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # en prod restringe dominios
    allow_credentials=True,
    allow_methods=["*"],           # permite todos los métodos (incluye OPTIONS)
    allow_headers=["*"],           # permite todos los headers
    expose_headers=["*"],
    max_age=600,
)

# --- Handler global para cualquier OPTIONS ---
@app.options("/{path:path}", include_in_schema=False)
def options_catch_all(path: str):
    return Response(
        status_code=204,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,PUT,PATCH,DELETE,OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "600",
        },
    )
# ----------------------------------------------

# Registrar rutas
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
