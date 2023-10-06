from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from utilitarios import conexion
from flask_cors import CORS
from os import environ
from dotenv import load_dotenv
from models import *
from flasgger import Swagger
from urllib.parse import quote_plus
from controllers import (RegistrosController , 
                         CategoriasController , 
                         RegistroController,
                         ProductosController, 
                         SubirImagenController,
                         DevolverImagenController,
                         CategoriaController,
                         ProductoController,
                         PedidosController,
                         LoginController, CambiarPasswordController,
                         PedidosController,UsuarioController, 
                         EnviarMensaje)


from flask_jwt_extended import JWTManager
# convierte un string en formato json a un diccionario
from json import load
from datetime import timedelta

# sirve para cargar mis variables declaradas en el archivo .env como si fueran variables de entorno
load_dotenv()
swaggerData = load(open('swagger_data.json', 'r'))

# https://github.com/flasgger/flasgger#customize-default-configurations
swaggerConfig = {
    'headers': [], # las cabeceras que van a aceptar nuestra documentacion
    'specs': [
        {
            'endpoint': '', # el endpoint inicial de nuestra documentacion 
            'route': '/'
        }
    ],
    'static_url_path': '/flasgger_static', # cargar los archivos staticos que serian el css y js de la libreria
    # 'swagger_ui': True, # indicar si queremos cargar la interfaz grafica o no
    'specs_route' : '/documentacion' # el endpoint en el cual ahora se ingresara a mi swagger
}

app = Flask(__name__)

if environ.get("PYTHON_VERSION"):
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URL")
else:    
    passwordBd = environ.get("DATABASE_URL").split(":")[2].split("@localhost")[0]
    passwordConvertida = quote_plus(passwordBd)
    urlBd = environ.get("DATABASE_URL").replace(passwordBd, passwordConvertida)
    #print(passwordBd)
    app.config['SQLALCHEMY_DATABASE_URI'] = urlBd

# servira para firmar las tokens
app.config['JWT_SECRET_KEY'] = "muysecreto"
app.config["JWT_ALGORITHM"] = "HS256"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1, minutes=15)


JWTManager(app)

Swagger(app, template=swaggerData, config=swaggerConfig)
# CORS > Cross Origin Resource Sharing (sirve para indicar quien puede tener acceso a mi API, indicando el dominio (origins), las cabeceras (allow_headers), y los metodos (methods))
CORS(app, origins='*')
api = Api(app)

conexion.init_app(app)

Migrate(app, conexion)

# rutas
api.add_resource(CategoriasController, '/categorias') 
api.add_resource(CategoriaController, '/categoria/<int:id>')
api.add_resource(RegistrosController, '/registro')
api.add_resource(RegistroController, '/registro/<int:id>')
api.add_resource(LoginController, '/login')
api.add_resource(SubirImagenController, '/subir-imagen')
api.add_resource(DevolverImagenController, '/imagenes/<nombreImagen>')
api.add_resource(ProductosController, '/productos')
api.add_resource(ProductoController, '/productos/<int:id>')
api.add_resource(PedidosController, '/pedidos')
api.add_resource(CambiarPasswordController, '/cambiar-contrasena')
api.add_resource(UsuarioController, '/perfil')
api.add_resource(EnviarMensaje, '/enviar-mensaje')


if __name__ == '__main__':
    app.run(debug=True)