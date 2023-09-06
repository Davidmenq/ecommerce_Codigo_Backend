from flask_restful import Resource, request
from utilitarios import conexion
from dtos import PedidoRequestDto
from flask_jwt_extended import get_jwt_identity
from decorators import validador_usuario_cliente
from models import PedidoModel, DetallePedidoModel

class PedidosController(Resource):

    @validador_usuario_cliente
    def post(self):
        data =request.get_json()
        try:
            dto = PedidoRequestDto()
            dataValidada = dto.load(data)
            usuarioId = get_jwt_identity()
            
            # TODO: buscar si existe esos productos en la base de datos

            # TODO: validar si hay stock suficiente para crear el pedido de ese producto 


            # primero creamos nuestro nuevo pedido
            nuevoPedido = PedidoModel(usuarioId = usuarioId, total = 0.0)

            conexion.session.add(nuevoPedido)
            conexion.session.commit()
            detallePedidos = dataValidada.get('detallePedido')

            total = 0.0

            for detallePedido in detallePedidos:
                # ahora itero mis detallesPedidos para ir guardandolos en la base de datos
                nuevoDetallePedido = DetallePedidoModel(productoId = detallePedido.get('productoId'), 
                                cantidad = detallePedido.get('cantidad'),
                                precio = detallePedido.get('precio'),
                                subTotal = detallePedido.get('cantidad') * detallePedido.get('precio'),
                                pedidoId = nuevoPedido.id
                                )
                # TODO: luego de agregar el detalle de pedido, disminuir el stock de ese producto

                # extraigo sus totales
                total += nuevoDetallePedido.subTotal
                # total = total + nuevoDetallePedido.subTotal
                conexion.session.add(nuevoDetallePedido)
            
            # modifico el total general de mi pedido con la sumatorio de mis detalles
            nuevoPedido.total = total
            
            conexion.session.commit()
            
            return {
                'message': 'Pedido creado correctamente'
            },201

        except Exception as error:
            conexion.session.rollback()
            
            return {
                'message': 'Error al crear el pedido',
                'content': error.args
            }