from marshmallow import Schema, fields

class DetallePedidoRequestDto(Schema):
    productoId = fields.Integer(required=True)
    cantidad = fields.Integer(required=True)
    precio = fields.Float(required=True)
    

class PedidoRequestDto(Schema):
    # primero definimos una lista y dentro de esa lista indicaremos que usaremos un Schema aninado en el cual definiremos nuestro schema para reutilizar
    detallePedido = fields.List(cls_or_instance = fields.Nested(nested = DetallePedidoRequestDto()))