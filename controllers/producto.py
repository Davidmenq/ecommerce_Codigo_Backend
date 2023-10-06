from flask_restful import Resource, request
from models import ProductoModel, CategoriaModel
from decorators import validador_usuario_admin
from dtos import ProductoRequestDto, ProductoResponseDto
from utilitarios import conexion

class ProductosController(Resource):

    @validador_usuario_admin
    def post(self):
        """
        file: documentacion/postProducto.yml
        """
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
        """
        file: ../documentacion/getProducto.yml
        """
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
    
class ProductoController(Resource):
    def get(self,id):
        """
        file: ../documentacion/getProductoId.yml
        """
        # SELECT * FROM productos;
        productoEncontrados  = conexion.session.query(ProductoModel).filter_by(id=id).join(CategoriaModel).first()
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
        return  dto.dump(productoEncontrados)
    
    @validador_usuario_admin
    def put(self,id):
        """
        file: documentacion/putProductoId.yml
        """
        categoriaEncontrada = conexion.session.query(ProductoModel).filter_by(id=id).first()
        if not categoriaEncontrada:
            return {
                 'message': 'El producto no existe'
             }, 404
        data = request.get_json()

        dto = ProductoRequestDto() 
        try:
            dataValidada = dto.load(data)
            # UPDATE usuarios SET nombre='...', apellido='...' ... WHERE id = '...';
            usuarioActualizados = conexion.session.query(ProductoModel).filter_by(id=id).update(dataValidada)

            print(usuarioActualizados)

            conexion.session.commit()

            return {
                'message': 'Producto Actualizado exitosamente'
            }
        
        except Exception as error:
            return {
                'message': 'Error al actualizar el producto',
                'content': error.args
            }  
    @validador_usuario_admin
    def delete(self,id):
        """
        file: documentacion/deleteProductoId.yml
        """
        categoriaEncontrada = conexion.session.query(ProductoModel).filter_by(id=id).first()
        if not categoriaEncontrada:
            return {
                 'message': 'El producto no existe no existe'
             }, 404

        try:
            categoriaEncontrada = conexion.session.query(ProductoModel).filter_by(id=id).delete()
            print(categoriaEncontrada)

            conexion.session.commit()

            return {
                'message': 'Producto eliminado exitosamente'
            }
        
        except Exception as error:
            return {
                'message': 'Error al eliminar el producto',
                'content': error.args
            }    

               