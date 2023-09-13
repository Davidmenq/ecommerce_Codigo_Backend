from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from marshmallow import fields, Schema
from models import UsuarioModel, TipoUsuario
from marshmallow_enum import EnumField


class UsuarioRequestDto(SQLAlchemyAutoSchema):
    # correo = auto_field() # cuando queremos agregar solamente para lectura o escritura
    # Sobrescribo mi atributo correo y le agrego validaciones adicionales (tiene que ser correo valido)
    correo = fields.Email(required=True)

    class Meta:
        model = UsuarioModel

class UsuarioResponseDto(SQLAlchemyAutoSchema):
    tipoUsuario = EnumField(TipoUsuario)
    password = auto_field(load_only=True) # solamente servira cuando se utilice para el metodo load y no para el metodo dump

    class Meta:
        model = UsuarioModel
        
class LoginRequestDto(Schema):
    correo = fields.Email(required=True)
    password = fields.Str(required=True)        

class CambiarPasswordRequestDto(Schema):
    password = fields.Str(required=True)
    nuevoPassword = fields.Str(required=True)