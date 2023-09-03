from utilitarios import conexion
from sqlalchemy import Column, types, ForeignKey
from datetime import datetime

class PedidoModel(conexion.Model):
    id = Column(type_=types.Integer, autoincrement=True, primary_key=True)
    fechaCreacion = Column(type_=types.DateTime, default= datetime.now, name='fecha_creacion')
    total = Column(type_=types.Float, nullable=False)
    usuarioId = Column(ForeignKey('usuarios.id'), name='usuario_id', type_=types.Integer, nullable=False)

    __tablename__ = 'pedidos'