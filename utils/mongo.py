from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

_client = None
_db = None

def get_mongo_client() -> MongoClient:
    """Retorna un cliente MongoDB singleton."""
    global _client
    if _client is None:
        if not MONGODB_URI:
            raise RuntimeError("MONGODB_URI no está definido en .env")
        _client = MongoClient(MONGODB_URI)
    return _client

def get_db():
    """Retorna el objeto de base de datos configurado."""
    global _db
    if _db is None:
        if not DATABASE_NAME:
            raise RuntimeError("DATABASE_NAME no está definido en .env")
        _db = get_mongo_client()[DATABASE_NAME]
    return _db

def get_collection(name: str):
    """Obtiene una colección por nombre."""
    return get_db()[name]

def t_connection() -> bool:
    """Hace ping a MongoDB para verificar conectividad."""
    try:
        get_mongo_client().admin.command("ping")
        return True
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return False
    
db = get_db()

def test_connection() -> bool:  # ← alias para compatibilidad
    return t_connection()




##from pymongo import MongoClient
#from dotenv import load_dotenv
#import os

#load_dotenv()

#client = MongoClient(os.getenv("MONGODB_URI"))
#db = client[os.getenv("DATABASE_NAME")]

#def get_collection(col):
#    """Obtiene una colección de MongoDB"""
#    client = get_mongo_client()
#    return client[DB][col]

#def test_connection():
#    try:
#        client = get_mongo_client()
#        client.admin.command("ping")
#        return True
#    except Exception as e:
#       print(f"Error connecting to MongoDB: {e}")
#        return False
#import os
#from dotenv import load_dotenv
#from pymongo import MongoClient
#from pymongo.server_api import ServerApi

#load_dotenv()

##DB = os.getenv("DATABASE_NAME")
#MONGODB_URI = os.getenv("MONGODB_URI")

#def get_collection( col ):
 #   client = MongoClient(  
  #      MONGODB_URI
   #     , server_api = ServerApi("1")
    #    , tls = True
     #   , tlsAllowInvalidCertificates = True
    #)
    #client.admin.command("ping")
   ## return client[DB][col]