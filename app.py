# app.py sin sqlalchemy , s eva a conectyar a mysql.connector cia conexion/conexion.py
from forms import ProductoForm
from flask import Flask, render_template, request, redirect, url_for, flash, session
from conexion.conexion import conexion, cerrar_conexion 
from forms import ProductoForm 
from datetime import datetime 
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import session, redirect, url_for, flash

app = Flask(__name__)
app.config['SECRET_KEY']= 'dev-secret-key'  # en producción usa variable de entorno

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "usuario" not in session:
            flash("⚠️ Debes iniciar sesión primero.", "warning")
            return redirect(url_for("iniciar_sesion"))
        return f(*args, **kwargs)
    return decorated_function

# Inyectar "now" para usar {{ now().year }} en templates si quieres
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}

# --- Rutas existentes ---
@app.route('/')
def index():
    return render_template('index.html', title='Inicio')

@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Bienvenido, {nombre}!'

@app.route('/about/')
def about():
    return render_template('about.html', title='Acerca de')

# ---------- REGISTRO ----------
@app.route("/registrarse", methods=["GET", "POST"]) 
def registrarse(): 
    if request.method == "POST": 
        usuario = request.form["usuario"] 
        correo = request.form["correo"] 
        password = request.form["password"] 
        
        conn = conexion() 
        cursor = conn.cursor(dictionary=True)  
        
        cursor.execute("SELECT * FROM usuarios WHERE usuario=%s OR correo=%s", (usuario, correo)) 
        existente = cursor.fetchone() 
        
        if existente: 
            flash("⚠️ El usuario o correo ya existen. Intenta con otros.", "danger") 
            cursor.close() 
            conn.close() 
            
            return redirect(url_for("registrarse")) 
        
        # Guardar usuario con contraseña encriptada 
        hash_pass = generate_password_hash(password) 
        cursor.execute("INSERT INTO usuarios (usuario, correo, password) VALUES (%s, %s, %s)", 
                       (usuario, correo, hash_pass)) 
        conn.commit() 
        cursor.close() 
        conn.close() 
        
        flash("✅ Usuario registrado con éxito. Ahora puedes iniciar sesión.", "success") 
        return redirect(url_for("iniciar_sesion")) 
    
    return render_template("registrarse.html")

# ---------- LOGIN ----------
@app.route("/iniciar_sesion", methods=["GET", "POST"])
def iniciar_sesion():
    if request.method == "POST":
        usuario_input = request.form.get("usuario")
        password = request.form.get("password")

        if not usuario_input or not password:
            flash("Complete todos los campos")
            return redirect(url_for("iniciar_sesion"))

        # Consultar MySQL directamente
        conn = conexion()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE usuario=%s OR correo=%s", (usuario_input, usuario_input))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["usuario"] = user["usuario"]  # coincidiendo con lo que usas en otras rutas
            flash("Inicio de sesión exitoso")
            return redirect(url_for("inicio"))
        else:
            flash("Usuario o contraseña incorrecta")
            return redirect(url_for("iniciar_sesion"))

    return render_template("login.html")

@app.route("/inventario")
@login_required
def inventario():
    return render_template("inventario.html")

# ---------- PÁGINA PRINCIPAL ----------
@app.route("/inicio")
def inicio():
    if "usuario" not in session:
        flash("⚠️ Debes iniciar sesión primero.", "warning")
        return redirect(url_for("iniciar_sesion"))
    return render_template("index.html", usuario=session["usuario"])


# ---------- CERRAR SESIÓN ----------
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("iniciar_sesion"))



    # GET → mostrar el formulario
    return render_template("login.html")

# ---------- Rutas de Platos ----------
@app.route('/platos')
@login_required
def listar_platos():
    conn = conexion()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM platos")
    platos = cur.fetchall()
    cerrar_conexion(conn)
    return render_template('platos/platos.html', title='Platos', platos=platos, q='')

@app.route('/platos/buscar')
def buscar_platos():
    q = request.args.get('q', '').strip()
    conn = conexion()
    cur = conn.cursor(dictionary=True)
    if q:
        cur.execute("SELECT * FROM platos WHERE nombre LIKE %s", (f"%{q}%",))
    else:
        cur.execute("SELECT * FROM platos")
    platos = cur.fetchall()
    cerrar_conexion(conn)
    return render_template('platos/platos.html', title='Buscar Platos', platos=platos, q=q)

@app.route("/carta")
def carta():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM platos")
    platos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("carta.html", platos=platos)

# ---- Productos ----
@app.route('/productos')
@login_required
def listar_productos():
    q = request.args.get('q', '').strip()
    conn = conexion()
    cur = conn.cursor(dictionary=True)
    if q:
        cur.execute("SELECT id, nombre, cantidad, precio FROM productos WHERE nombre LIKE %s", (f"%{q}%",))
    else:
        cur.execute("SELECT id, nombre, cantidad, precio FROM productos")
    productos = cur.fetchall()
    cerrar_conexion(conn)
    return render_template('productos/lista.html', title='Productos', productos=productos, q=q)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def crear_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        conn = conexion()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO productos (nombre, cantidad, precio) VALUES (%s, %s, %s)",
                (form.nombre.data, form.cantidad.data, float(form.precio.data))
            )
            conn.commit()
            flash('Producto agregado correctamente.', 'success')
            return redirect(url_for('listar_productos'))
        except Exception as e:
            conn.rollback()
            form.nombre.errors.append('No se pudo guardar: ' + str(e))
        finally:
            cerrar_conexion(conn)
    return render_template('productos/form.html', title='Nuevo producto', form=form, modo='crear')


@app.route('/productos/<int:pid>/editar', methods=['GET', 'POST'])
def editar_producto(pid):
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, cantidad, precio FROM productos WHERE id = %s", (pid,))
    prod = cursor.fetchone()
    if not prod:
        cerrar_conexion(conn)
        return "Producto no encontrado", 404
    form = ProductoForm(data={'nombre': prod[1], 'cantidad': prod[2], 'precio': prod[3]})
    if form.validate_on_submit():
        nombre = form.nombre.data.strip()
        cantidad = form.cantidad.data
        precio = form.precio.data
        try:
            cursor.execute("UPDATE productos SET nombre=%s, cantidad=%s, precio=%s WHERE id=%s", 
                           (nombre, cantidad, precio, pid))
            conn.commit()
            flash('Producto actualizado correctamente.', 'success')
            return redirect(url_for('listar_productos'))
        except Exception as e:
            conn.rollback()
            form.nombre.errors.append('Error al actualizar el producto. Puede que ya exista otro con ese nombre.')
        finally:
            cerrar_conexion(conn)
    cerrar_conexion(conn)
    return render_template('productos/form.html', title='Editar producto', form=form, modo='editar', pid=pid)

@app.route('/productos/<int:pid>/eliminar', methods=['POST'])
def eliminar_producto(pid):
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (pid,))
    if cursor.rowcount > 0:
        conn.commit()
        flash('Producto eliminado correctamente.', 'success')
    else:
        flash('Producto no encontrado.', 'warning')
    cerrar_conexion(conn)
    return redirect(url_for('listar_productos'))

if __name__ == '__main__':
    app.run(debug=True)