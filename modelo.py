# modelo de flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f'<Producto {self.nombre}>'

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<Categoria {self.nombre}>'