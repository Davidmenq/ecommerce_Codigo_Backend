from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from models import ProductoModel
from dtos import CategoriaRequestDto

class ProductoRequestDto(SQLAlchemyAutoSchema):
    class Meta:
        model = ProductoModel
        # para incluir las llaves foraneas al momento de hacer la validacion
        include_fk = True

class ProductoResponseDto(SQLAlchemyAutoSchema):
    categoria = fields.Nested(CategoriaRequestDto)

    class Meta:
        model = ProductoModel