from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models import CategoriaModel

class CategoriaRequestDto(SQLAlchemyAutoSchema):
    class Meta:
        model = CategoriaModel