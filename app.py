# rutas en flask
from flask import Flask

app = Flask(__name__)
@app.route('/')
def index():
    return "_Hola mundo!"
@app.route('/about')
def about():
    return "Acerca de nosotros"  
@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Bienvenido, {nombre}!'
if __name__ == '__main__':
    app.run(debug=True)
    # ejecutar con el comando: python app.py