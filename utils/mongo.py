from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client[os.getenv("DATABASE_NAME")]

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