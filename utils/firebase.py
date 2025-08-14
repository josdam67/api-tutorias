# utils/firebase.py
import os
import json
import base64
import firebase_admin
from firebase_admin import credentials, auth

_APP = None

def _normalize_b64(s: str) -> str:
    # Quita espacios/saltos y corrige padding '='
    s = s.strip().replace("\n", "").replace("\r", "").replace(" ", "")
    missing = (-len(s)) % 4
    if missing:
        s += "=" * missing
    return s

def _init_firebase():
    """Inicializa Firebase una sola vez (lazy init)."""
    global _APP
    if _APP is not None:
        return _APP
    if firebase_admin._apps:
        _APP = firebase_admin.get_app()
        return _APP

    b64 = os.getenv("FIREBASE_CREDENTIALS_BASE64")
    cred_path = os.getenv(
        "FIREBASE_CREDENTIALS_PATH",
        os.path.join("secrets", "tutorias-secrets.json")  # ruta local por defecto
    )

    if b64:
        try:
            b64n = _normalize_b64(b64)
            raw = base64.b64decode(b64n)
            data = json.loads(raw)              # ← JSON válido
            cred = credentials.Certificate(data)  # ← admite dict
        except Exception as e:
            raise RuntimeError(f"Error decodificando FIREBASE_CREDENTIALS_BASE64: {e}")
    else:
        if not os.path.exists(cred_path):
            raise FileNotFoundError(
                f"Credenciales Firebase no encontradas. "
                f"Define FIREBASE_CREDENTIALS_BASE64 o crea el archivo en: {cred_path}"
            )
        cred = credentials.Certificate(cred_path)

    _APP = firebase_admin.initialize_app(cred)
    return _APP

def create_firebase_user(email: str, password: str):
    _init_firebase()
    user = auth.create_user(email=email, password=password)
    return user.uid

def verify_firebase_token(id_token: str):
    _init_firebase()
    decoded_token = auth.verify_id_token(id_token)
    return decoded_token
