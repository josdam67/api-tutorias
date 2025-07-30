import firebase_admin
from firebase_admin import credentials, auth
import os


cread_path = os.path.join("secrets", "tutorias-secrets.json") #pendiente creacion
if not firebase_admin._apps:
    cred = credentials.Certificate(cread_path)
    firebase_admin.initialize_app(cred)


def create_firebase_user(email: str, password: str):
    user = auth.create_user(email=email, password=password)
    return user.uid

def verify_firebase_token(id_token: str):
    decoded_token =auth.verify_id_token(id_token)
    return decoded_token