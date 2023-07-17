from sqlalchemy import Column, Integer, String, Date, Enum, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Usuarios(Base):
    __tablename__ = "Usuarios"

    Id_usuario =  Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50), index=True)
    apellido = Column(String(50), index=True)
    email = Column(String(100), unique=True, index=True)
    fecha_nacimiento = Column(Date)
    genero = Column(Enum('M', 'F', name='genero'))
    direccion = Column(String(255))
    telefono = Column(String(20), unique=True)
    cedula = Column(String(20), unique=True)
    pais = Column(String(50))
    region = Column(String(50))
