from flask_restful import Resource, request
from decorators import validador_usuario_admin
from os import path
from werkzeug.utils import secure_filename 
from datetime import datetime
from flask import send_file
import boto3

class SubirImagenController(Resource):

    # si utilizamos el decorador personalizado y este se ubica en otra posicion del proyecto entonces tendremos que setear el archivo de swagger en la ubicacion de ese decorador
    @validador_usuario_admin
    def post(self):
        # Conéctate a AWS S3
        s3 = boto3.client(
    's3',
    aws_access_key_id='YOUR_ACCESS_KEY_ID',
    aws_secret_access_key='YOUR_SECRET_ACCESS_KEY',
    region_name='YOUR_REGION'
)

        print(request.files.get('imagen'))
        imagen = request.files.get('imagen')

        mimetypeValidos = ['image/png', 'image/jpeg', 'image/svg+xml']

        if not imagen:
            return {
                'message': 'Se necesita una imagen'
            }, 400
        
        print(imagen.filename)
        print(imagen.name)
        print(imagen.mimetype)
        
        if imagen.mimetype not in mimetypeValidos:
            return {
                'message': 'El archivo solo puede ser .jpg, .png, .svg'
            }, 400
        
        # Genera un nombre de archivo único
        id = datetime.now().strftime('%f')
        filename = id + imagen.filename 

        try:
            # Sube la imagen a AWS S3
            s3.upload_fileobj(imagen, 'bucket1810', filename)
        except Exception as e:
            return {
                'message': 'Error al subir la imagen a AWS S3'
            }, 500

        # URL de la imagen en S3
        s3_url = f'https://bucket1810.s3.us-west-2.amazonaws.com/{filename}'

        return {
            'message': 'Imagen subida exitosamente',
            'content': {
                'imagen': s3_url
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