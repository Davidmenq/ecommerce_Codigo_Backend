from flask_restful import Resource, request
from decorators import validador_usuario_admin
from os import path
from werkzeug.utils import secure_filename 
from datetime import datetime
from flask import send_file

class SubirImagenController(Resource):

    # si utilizamos el decorador personalizado y este se ubica en otra posicion del proyecto entonces tendremos que setear el archivo de swagger en la ubicacion de ese decorador
    @validador_usuario_admin
    def post(self):
        """
        file: documentacion/subirImagenSwagger.yml
        """
        # path.join > sirve para unir varias carpetas y archivos en un formato que pueda ser legible por el sistema operativo
        # c:\\user\\eduardo > linux
        # c:/user/eduardo   > ps (windows)
        # c:\user\eduardo   > cmd (windows)
        print(request.files.get('imagen'))
        imagen = request.files.get('imagen')

        # https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types
        mimetypeValidos = ['image/png', 'image/jpeg', 'image/svg+xml']

        if not imagen:
            return {
                'message': 'Se necesita una imagen'
            }, 400
        
        # validar tipos de archivos
        print(imagen.filename) # nombre del archivo
        print(imagen.name) # nombre de la llave de en mi form-data
        print(imagen.mimetype)
        if imagen.mimetype not in mimetypeValidos:
            return {
                'message': 'El archivo solo puede ser .jpg, .png, .svg'
            }, 400
        
        # extrae el microsegundo de la hora actual
        id = datetime.now().strftime('%f')
        # quita algun caracter que pueda generar conflictos al momento de buscar el archivo en el servidor
        filename = id + secure_filename(imagen.filename) 

        # procedemos con el guardado de la imagen
        ruta = path.join('imagenes', filename)
        imagen.save(ruta)

        return {
            'message': 'Imagen subida exitosamente',
            'content': {
                'imagen': f'http://localhost:5000/imagenes/{filename}' 
            }
        }


class DevolverImagenController(Resource):

    def get(self, nombreImagen):
        ruta = path.join('imagenes',nombreImagen)

        # validamos si tenemos el archivo en nuestro servidor
        resultado = path.isfile(ruta)

        if not resultado:
            return {
                'message': 'El archivo a buscar no existe'
            }, 404
        
        # sirve para enviar un archivo en particular para que lo pueda leer el cliente
        return send_file(ruta)