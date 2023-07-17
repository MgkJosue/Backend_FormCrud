from pydantic import BaseModel, validator
from datetime import date, datetime
import re

class UserBase(BaseModel):
    nombre: str
    apellido: str
    email: str
    fecha_nacimiento: date
    genero: str
    direccion: str
    telefono: str
    cedula: str
    pais: str
    region: str

    @validator('cedula')
    def validate_cedula(cls, v):
        if len(v) != 10 or not re.match(r'^\d{10}$', v):
            raise ValueError('Cédula inválida')
        impares = [int(d) for d in v[:9:2]]
        impares = [d * 2 if d < 5 else d * 2 - 9 for d in impares]
        pares = [int(d) for d in v[1:8:2]]
        total = sum(impares) + sum(pares)
        verificador = 0 if total % 10 == 0 else 10 - (total % 10)
        if int(v[9]) != verificador:
            raise ValueError('Cédula inválida')
        return v

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    pass

class User(UserBase):
    Id_usuario: int

    class Config:
        orm_mode = True
