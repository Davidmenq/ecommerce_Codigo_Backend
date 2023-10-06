from flask_restful import Resource, request
from mensajeria import enviarMensaje
from os import environ



class EnviarMensaje(Resource):

    def post(self):

        data = request.get_json()
        
        print(data)        

        enviarMensaje(data)
        