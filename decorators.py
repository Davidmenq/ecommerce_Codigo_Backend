from functools import wraps

from flask_jwt_extended.view_decorators import verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from models import UsuarioModel, TipoUsuario
from utilitarios import conexion


# custom decorator
def validador_usuario_admin(funcion):
    # wraps > envuelve la funcion o metodo donde vamos a utlizar esta funcion para devolvernos toda su configuracion (parametros y otros)
    @wraps(funcion)
    def wrapper(*args, **kwargs):
        # es donde voy a hacer la validacion

        # decodifica la token de la peticion (de los headers de autorizacion)
        data = verify_jwt_in_request()

        id = data[1].get('sub')

        usuarioEncontrado = conexion.session.query(
            UsuarioModel).filter_by(id=id).first()

        if not usuarioEncontrado:
            raise NoAuthorizationError('El usuario no existe')

        print(usuarioEncontrado.tipoUsuario)
        if usuarioEncontrado.tipoUsuario != TipoUsuario.ADMIN:
            raise NoAuthorizationError(
                'El usuario no tiene los permisos suficientes')

        # si la validacion es exitosa lo dejare pasar a la funcion que viene despues del decorador
        return funcion(*args, **kwargs)
    
    return wrapper



def validador_usuario_cliente(funcion):
    @wraps(funcion)
    def wrapper(*args, **kwargs):
        data = verify_jwt_in_request()

        id = data[1].get('sub')

        usuarioEncontrado = conexion.session.query(
            UsuarioModel).filter_by(id=id).first()

        if not usuarioEncontrado:
            raise NoAuthorizationError('El usuario no existe')

        if usuarioEncontrado.tipoUsuario != TipoUsuario.CLIENTE:
            raise NoAuthorizationError(
                'El usuario no tiene los permisos suficientes')

        return funcion(*args, **kwargs)

    return wrapper

def validador_usuario_logueado(funcion):
    @wraps(funcion)
    def wrapper(*args, **kwargs):
        data = verify_jwt_in_request()

        id = data[1].get('sub')

        usuarioEncontrado = conexion.session.query(
            UsuarioModel).filter_by(id=id).first()

        if not usuarioEncontrado:
            raise NoAuthorizationError('El usuario no existe')

        return funcion(*args, **kwargs)

    return wrapper