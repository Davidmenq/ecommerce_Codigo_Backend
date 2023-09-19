from utilitarios import conexion
from sqlalchemy import Column, ForeignKey, types
from sqlalchemy.orm import relationship

class ProductoModel(conexion.Model):
    __tablename__='productos'

    id = Column(type_=types.Integer, primary_key=True, autoincrement=True)
    nombre = Column(type_=types.Text, nullable=False)
    descripcion = Column(type_=types.Text)
    precio = Column(type_=types.Float, nullable=False)
    imagenes = Column(type_=types.ARRAY(types.Text)) 
    disponibilidad = Column(type_=types.Boolean, default=True)
    stock = Column(type_=types.Integer, nullable=False)
    categoriaId = Column(ForeignKey(column='categorias.id'), type_=types.Integer
    , name='categoria_id')
    
    # es el nombre de la clase!
    # backref > crea un atributo virtual (se crea al momento de llamar a una/muchas categoria en la clase CategoriaModel)
    categoria = relationship('CategoriaModel', backref='productos')