from flask_restful import Resource, request
from utilitarios import conexion
from dtos import PedidoRequestDto
from flask_jwt_extended import get_jwt_identity
from decorators import validador_usuario_cliente
from models import PedidoModel, DetallePedidoModel , ProductoModel

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
                producto_id = detallePedido.get('productoId')
                cantidad = detallePedido.get('cantidad')
                
                # Consultar la tabla de productos para obtener el precio
                producto = ProductoModel.query.filter_by(id=producto_id).first()
                
                if producto:
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
                    
                    # Agregar el detalle a la base de datos
                    conexion.session.add(nuevoDetallePedido)
                else:
                    # Manejar el caso en el que no se encuentra el producto en la base de datos
                    # Puedes agregar una lógica para manejar esto según tus necesidades
                    pass
                
                                                                
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