from sqlalchemy import Column, types
from utilitarios import conexion
from datetime import datetime

class CategoriaModel(conexion.Model):
    id = Column(type_=types.Integer, primary_key=True, autoincrement=True)
    nombre = Column(type_=types.Text, nullable=True)
    fechaCreacion = Column(type_=types.DateTime, default=datetime.now, name='fecha_creacion')
    imagen = Column(type_=types.Text)

    __tablename__='categorias'