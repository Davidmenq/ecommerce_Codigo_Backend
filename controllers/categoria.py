from flask_restful import Resource, request
from models import CategoriaModel 
from dtos import CategoriaRequestDto 
from utilitarios import conexion
from decorators import validador_usuario_admin
# get_jwt_identity > devolvera la identificacion del usuario de la token
from flask_jwt_extended import jwt_required, get_jwt_identity


class CategoriasController(Resource):

    @validador_usuario_admin
    def post(self):
        """
        file: documentacion/postCategoria.yml
        """
        dto = CategoriaRequestDto()
        # identificador = get_jwt_identity()
        # print(identificador)
        
        try:
            dataVerificada = dto.load(request.get_json())
            nuevaCategoria = CategoriaModel(**dataVerificada)
            conexion.session.add(nuevaCategoria)
            conexion.session.commit()
            return {
                'message': 'Categoria creada exitosamente',
                'content': ''
            }, 201
        
        except Exception as e:
            # rollback > retroceder el estado antes de que se de el error en la base de datos
            conexion.session.rollback()
            return{
                'message': 'Error al crear la categoria',
                'content': e.args
            }, 400

    def get(self):
        """
        file: ../documentacion/getCategoria.yml
        """
        categorias = conexion.session.query(CategoriaModel).all()
        dto = CategoriaRequestDto()
        resultado =dto.dump(categorias, many=True)

        return resultado , 200
    
class CategoriaController(Resource):    
    
    def get(self,id):
        """
        file: ../documentacion/getCategoriaId.yml
        """
        categoriaEncontrada = conexion.session.query(CategoriaModel).filter_by(id=id).first()
        
        if not categoriaEncontrada:
            return {
                 'message': 'La categoria no existe'
             }, 404
        dto = CategoriaRequestDto() 
        categoria = dto.dump(categoriaEncontrada)  

        return categoria
    
    @validador_usuario_admin
    def put(self,id):
        """
        file: documentacion/putCategoriaId.yml
        """
        print(f'Imprime el parametro ID y su tipo: {id} {type(id)}')
        categoriaEncontrada = conexion.session.query(CategoriaModel).filter_by(id=id).first()
        print(categoriaEncontrada)
        if not categoriaEncontrada:
            return {
                 'message': 'La categoria no existe'
             }, 404
        data = request.get_json()

        dto = CategoriaRequestDto() 
        try:
            dataValidada = dto.load(data)
            # UPDATE usuarios SET nombre='...', apellido='...' ... WHERE id = '...';
            usuarioActualizados = conexion.session.query(CategoriaModel).filter_by(id=id).update(dataValidada)

            print(usuarioActualizados)

            conexion.session.commit()

            return {
                'message': 'Categoria actualizada exitosamente'
            }
        
        except Exception as error:
            return {
                'message': 'Error al actualizar la categoria',
                'content': error.args
            }  
    
    @validador_usuario_admin
    def delete(self,id):
        """
        file: documentacion/deleteCategoriaId.yml
        """
        categoriaEncontrada = conexion.session.query(CategoriaModel).filter_by(id=id).first()
        if not categoriaEncontrada:
            return {
                 'message': 'La categoria no existe'
             }, 404

        try:
            categoriaEncontrada = conexion.session.query(CategoriaModel).filter_by(id=id).delete()
            print(categoriaEncontrada)

            conexion.session.commit()

            return {
                'message': 'Categoria eliminada exitosamente'
            }
        
        except Exception as error:
            return {
                'message': 'Error al eliminar la categoria',
                'content': error.args
            } 
          