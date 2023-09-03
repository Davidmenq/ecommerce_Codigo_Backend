from flask_restful import Resource, request
from models import ProductoModel, CategoriaModel
from decorators import validador_usuario_admin
from dtos import ProductoRequestDto, ProductoResponseDto
from utilitarios import conexion

class ProductosController(Resource):

    def post(self):
        data = request.get_json()
        dto = ProductoRequestDto()
        try:
            dataValidada = dto.load(data)

            nuevoProducto = ProductoModel(**dataValidada)

            conexion.session.add(nuevoProducto)
            conexion.session.commit()
            dtoRpta = ProductoResponseDto()
            
            return {
                'message': 'Producto creado exitosamente',
                'content': dtoRpta.dump(nuevoProducto)
            }
        
        except Exception as error:
            conexion.session.rollback()
            return {
                'message': 'Error al crear el producto',
                'content': error.args
            },400
        
    def get(self):
        # SELECT * FROM productos;
        productoEncontrados  = conexion.session.query(ProductoModel).join(CategoriaModel).all()
        # SELECT productos.id, categorias.id, categoria.nombre FROM productos JOIN categorias ON productos.categoria_id = categorias.id
        # podemos indicar que columnas queremos obtener
        # NOTA: al hacer uso del with_entities se pierde la instancia y se devuelve en forma de tupla la informacion
        # el join al ya tener relationships se vuelve implicito a no ser que querramos crear un join inexistente
        data = conexion.session.query(ProductoModel).join(CategoriaModel).with_entities(ProductoModel.id, 
                                                                                        CategoriaModel.id, 
                                                                                        CategoriaModel.nombre).all()
        print(conexion.session.query(ProductoModel).join(CategoriaModel).with_entities(ProductoModel.id, 
                                                                                       CategoriaModel.id, 
                                                                                       CategoriaModel.nombre))
        
        dto = ProductoResponseDto()
        return  dto.dump(productoEncontrados, many=True)
               