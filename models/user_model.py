from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    #id_usuario: Optional[str] = Field(
      #  default=None,
       # description="MongoDB ID"
    #)
    nombre: str = Field(
        description="User First Name"
    )
    apellido: str = Field(
        description="User Last Name"
    )
    email: EmailStr

    tipo_usuario: str = Field (
        description= "Tipo de usuario, Admin, Tutor, Estudiante"
    )#recordando la recomendacion que me dio de que puede ser Admin, Tutor, Estudiante

    admin: bool = Field(
        default=False
    )

class UserCreate(UserBase):
    password: str


class UserDB(UserBase):
    id_usuario: str
    fecha_registro: datetime = Field(
        description="Fecha Registro "
    )
    activo: bool = Field(
        default= True 
    )

class FirebaseLogin(BaseModel):
    firebase_token: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
