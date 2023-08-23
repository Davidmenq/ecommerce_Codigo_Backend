from utilitarios import conexion
from sqlalchemy import Column, types
from enum import Enum
from datetime import datetime

class TipoUsuario(Enum):
    ADMIN = 'ADMIN'
    CLIENTE = 'CLIENTE'

class UsuarioModel(conexion.Model):
    id = Column(type_=types.Integer, primary_key=True, autoincrement=True)
    nombre = Column(type_=types.Text, nullable=False)
    correo = Column(type_=types.Text, nullable=False, unique=True)
    password = Column(type_=types.Text, nullable=False)
    tipoUsuario = Column(type_=types.Enum(TipoUsuario), nullable=False, name='tipo_usuario')
    birthday = Column(type_=types.Date)
    fechaCreacion = Column(type_=types.DateTime, default= datetime.now, name='fecha_creacion')
    __tablename__ = 'usuarios'