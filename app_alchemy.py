# rutas en flask
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from forms import ProductoForm
from wtforms.validators import DataRequired, Length
from inventario import Inventario

app = Flask(__name__)

#clave secreta para formularios
app.config['SECRET_KEY'] = 'clave_secreta_2016'
#app.config['wtf_CSRF_secret_key'] = ' clave_csrf_2016'

inventario = Inventario()
CSRFPROTECT_ENABLED = True

@app.route('/')
def index():
    return render_template('index.html', title="Página Principal")


@app.route('/inventario')
def ver_inventario():
    productos = [
        {'nombre': 'veviche de camaron', 'cantidad': 10, 'precio': 4.00},
        {'nombre': 'Arroz marinero', 'cantidad': 5, 'precio': 10.00}
    ]
    return render_template('inventario.html', productos=productos, titulo="Inventario")
@app.route('/about')
def about():
    return render_template('about.html', title="Acerca de") 

@app.route('/contactos')
def contactos():
    return render_template('contactos.html', title="Contactos")

@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Bienvenido, {nombre}!'



@app.route('/productos')
def listar_productos():
    q = request.get('q', '').strip()
    productos = inventario.buscar_productos_por_categoria(q) if q else inventario.listar_productos()
    return render_template('productos/lista.html', title="Productos", productos=productos, q=q)


@app.route('/producto/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        cantidad = form.cantidad.data
        precio = form.precio.data
        flash(f'Producto "{nombre}" con cantidad {cantidad} y precio {precio} añadido exitosamente.', 'success')
        return redirect(url_for('index'))

    return render_template('form.html', titulo="Nuevo Producto", form=form)

if __name__ == '__main__':
    app.run(debug=True)