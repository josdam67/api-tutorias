
from fastapi import HTTPException
from utils.firebase import create_firebase_user
from utils.jwt_handler import create_access_token
from datetime import datetime
from utils.mongo import db
from models.user_model import UserLogin
import os
import requests

# Colección de usuarios en Mongo
users_col = db["usuarios"]

def register_user(data):
    # Crea usuario en Firebase
    firebase_uid = create_firebase_user(data["email"], data["password"])

    # Guarda en Mongo
    user_doc = {
        "id_usuario": firebase_uid,
        "nombre": data["nombre"],
        "apellido": data["apellido"],
        "email": data["email"],
        "tipo_usuario": data["tipo_usuario"],
        "fecha_registro": datetime.utcnow(),
        "activo": True
    }
    users_col.insert_one(user_doc)

    return {"msg": "Usuario registrado correctamente", "id_usuario": firebase_uid}

def login_user(firebase_token: str):
    # Login usando id_token de Firebase
    from utils.firebase import verify_firebase_token
    decoded = verify_firebase_token(firebase_token)

    user = users_col.find_one({"email": decoded["email"]})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en MongoDB")

    payload = {
        "id_usuario": user["id_usuario"],
        "email": user["email"],
        "tipo_usuario": user["tipo_usuario"]
    }
    token = create_access_token(payload)
    return {"access_token": token, "token_type": "bearer"}

def login_datos(data: UserLogin):
    """
    Login con email/password (Firebase REST) + JWT propio.
    Devuelve el error exacto de Firebase si falla (INVALID_PASSWORD, EMAIL_NOT_FOUND, etc).
    """
    FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
    if not FIREBASE_API_KEY:
        # Config del servidor incompleta
        raise HTTPException(status_code=500, detail="FIREBASE_API_KEY no está configurada")

    firebase_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {
        "email": data.email,
        "password": data.password,
        "returnSecureToken": True,
    }

    # Llamada a Firebase con manejo de red
    try:
        r = requests.post(firebase_url, json=payload, timeout=15)
        result = r.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error conectando a Firebase: {e}")

    # Si Firebase respondió error, devolvemos el mensaje específico
    if r.status_code != 200:
        fb_msg = result.get("error", {}).get("message", "Credenciales inválidas")
        # Ejemplos: EMAIL_NOT_FOUND, INVALID_PASSWORD, USER_DISABLED, API_KEY_INVALID
        raise HTTPException(status_code=401, detail=f"Firebase: {fb_msg}")

    # Verificamos que exista el usuario en Mongo
    user = users_col.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en MongoDB")

    # Generamos JWT local
    payload_jwt = {
        "id_usuario": user["id_usuario"],
        "email": user["email"],
        "tipo_usuario": user["tipo_usuario"],
    }
    token = create_access_token(payload_jwt)

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "email": user["email"],
            "nombre": user["nombre"],
            "tipo_usuario": user["tipo_usuario"],
        },
    }
