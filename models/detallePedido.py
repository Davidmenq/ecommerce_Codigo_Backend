from sqlalchemy import Column,types, ForeignKey
from utilitarios import conexion

class DetallePedidoModel(conexion.Model):
    id = Column(type_=types.Integer, autoincrement=True, primary_key=True)
    cantidad = Column(type_=types.Integer, nullable=False)
    precio = Column(type_=types.Float, nullable=False)
    subTotal = Column(type_=types.Float, nullable=False ,name='sub_total')
    productoId = Column(ForeignKey('productos.id'),type_=types.Integer, nullable=False, name='producto_id')
    pedidoId = Column(ForeignKey('pedidos.id'),type_=types.Integer, nullable=False, name='pedido_id')

    __tablename__ = 'detalle_pedidos'
