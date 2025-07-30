from fastapi import HTTPException
from utils.firebase import create_firebase_user
from utils.jwt_handler import create_access_token
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
from utils.mongo import db
import os
from models.user_model import UserLogin
import requests
load_dotenv()

users_col = db["usuarios"]

def register_user(data):
    # aca estamos creando en firebase
    firebase_uid = create_firebase_user(data["email"], data["password"])

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
    from utils.firebase import verify_firebase_token
    decoded = verify_firebase_token(firebase_token)
    user = users_col.find_one({"email": decoded["email"]})
    if not user:
        raise Exception("Usuario no encontrado en MongoDB")

    payload = {
        "id_usuario": user["id_usuario"],
        "email": user["email"],
        "tipo_usuario": user["tipo_usuario"]
    }
    token = create_access_token(payload)
    return {"access_token": token, "token_type": "bearer"}



# def login_datos(data: UserLogin):
#     user = db["usuarios"].find_one({"email": data.email})

#     if not user:
#         raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
#     if "password"not in user or  user["password"] != data.password:
#         raise HTTPException(status_code=401, detail="Contrasena Incorrecta")
    
#     return{

#         "message": "Login exitoso",
#         "email": user["email"],
#         "nombre": user["nombre"],
#         "tipo_usuario": user["tipo_usuario"]

#     }

def login_datos(data: UserLogin):
    FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")

    firebase_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"

    payload = {
        "email": data.email,
        "password": data.password,
        "returnSecureToken": True
    }

    response = requests.post(firebase_url, json=payload)
    result = response.json()

    if "error" in result:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    # Aquí el usuario fue autenticado correctamente en Firebase

    user = db["usuarios"].find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en MongoDB")

    # Crea JWT local (propio)
    payload = {
        "id_usuario": user["id_usuario"],
        "email": user["email"],
        "tipo_usuario": user["tipo_usuario"]
    }

    token = create_access_token(payload)

    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {
            "email": user["email"],
            "nombre": user["nombre"],
            "tipo_usuario": user["tipo_usuario"]
        }
    }
