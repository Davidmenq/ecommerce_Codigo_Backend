from flask_restful import Resource, request
from mensajeria import enviarRutaCambiarContrasena
from os import environ



class RecuperarContrasenaController(Resource):

    def post(self):
        data = request.get_json()
        email = data.get('email')  # Obtiene el correo electrónico del cuerpo de la solicitud
        print(email)  # Imprime el correo electrónico en la consola para verificar
        #enviarRutaCambiarContrasena(email)
        # Llama a la función para enviar el correo electrónico
        enviarRutaCambiarContrasena(email)
        
        """ enviarRutaCambiarContrasena(data.get('email')) """
        """ email = data.get('email')  # Obtiene el correo electrónico del cuerpo de la solicitud
        print(email)  # Imprime el correo electrónico en la consola para verificar

        # Llama a la función para enviar el correo electrónico
        enviarRutaCambiarContrasena(email) """

        # Puedes devolver una respuesta JSON al frontend si es necesario
        """ return {'message': 'Correo electrónico enviado correctamente'}, 200 """
        
        