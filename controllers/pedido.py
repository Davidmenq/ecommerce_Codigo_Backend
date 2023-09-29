from flask_restful import Resource, request
from utilitarios import conexion
from dtos import PedidoRequestDto
from flask_jwt_extended import get_jwt_identity
from decorators import validador_usuario_cliente
from models import PedidoModel, DetallePedidoModel , ProductoModel

class PedidosController(Resource):

    @validador_usuario_cliente
    def post(self):
        data = request.get_json()
        try:
            dto = PedidoRequestDto()
            dataValidada = dto.load(data)
            usuarioId = get_jwt_identity()

            detallePedidos = dataValidada.get('detallePedido')

            # Verificar si hay suficiente stock para todos los productos en el detalle
            for detallePedido in detallePedidos:
                producto_id = detallePedido.get('productoId')
                cantidad = detallePedido.get('cantidad')
                producto = ProductoModel.query.filter_by(id=producto_id).first()

                if not producto or cantidad > producto.stock:
                    # No hay suficiente stock para este producto o el producto no existe
                    return {
                        'message': f'No hay suficiente stock para el producto con ID {producto_id} eliminalo para poder continuar con el pedido'
                    },400

            # Si llegamos aquí, significa que hay suficiente stock para todos los productos
            # Creamos un nuevo pedido
            nuevoPedido = PedidoModel(usuarioId=usuarioId, total=0.0)
            conexion.session.add(nuevoPedido)

            total = 0.0

            for detallePedido in detallePedidos:
                producto_id = detallePedido.get('productoId')
                cantidad = detallePedido.get('cantidad')
                producto = ProductoModel.query.filter_by(id=producto_id).first()

                precio = producto.precio
                sub_total = cantidad * precio

                # Crear un nuevo detalle de pedido con el precio calculado
                nuevoDetallePedido = DetallePedidoModel(
                    productoId=producto_id,
                    cantidad=cantidad,
                    precio=precio,
                    subTotal=sub_total,
                    pedidoId=nuevoPedido.id
                )
                conexion.session.add(nuevoDetallePedido)

                # Actualizar el stock del producto
                nuevoStock = producto.stock - cantidad
                producto.stock = nuevoStock

                # Actualizar el total del pedido
                total += nuevoDetallePedido.subTotal

            # Actualizar el total general de mi pedido con la sumatoria de los detalles
            nuevoPedido.total = total
            conexion.session.commit()

            return {
                'message': 'Pedido creado correctamente'
            }, 201

        except Exception as error:
            conexion.session.rollback()

            return {
                'message': 'Error al crear el pedido',
                'content': error.args
            }