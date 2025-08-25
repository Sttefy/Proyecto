# rutas en flask
from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html', title="Página Principal")
@app.route('/about')
def about():
    return render_template('about.html', title="Acerca de")  
@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Bienvenido, {nombre}!'
if __name__ == '__main__':
    app.run(debug=True)
    # ejecutar con el comando: python app.py