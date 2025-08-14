import pytest
from utils.mongo import get_collection, t_connection, get_mongo_client
import os
from dotenv import load_dotenv

load_dotenv()

def test_env_variables():
    mongodb_uri = os.getenv("MONGODB_URI")
    assert mongodb_uri is not None, "MONGODB_URI no está CONFIGURADO"
    print ( f"Database URI: {mongodb_uri}" )

def test_connect():
    try:
        connection_result = t_connection()
        assert connection_result is True, "La conexxion a la BD fallo"
    except Exception as e:
        pytest.fail( f"Error en la conexion de MongoDB {str(e)}")

def test_mongo_client():
    try:
        client = get_mongo_client()
        assert client is not None, "El cliente de Mongo is None"
    except Exception as e:
        pytest.fail( f"Error en el llamado del cliente {str(e)}")

def test_get_collection():
    try:
        users_col = get_collection("usuarios")
        assert users_col is not None, "Error al obtener la colección de usuarios"
    except Exception as e:
        pytest.fail( f"Error a; obtener/usar la coleccion {str (e)}")
