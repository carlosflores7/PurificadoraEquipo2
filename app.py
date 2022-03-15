import datetime
from datetime import timedelta

from flask import Flask,render_template,request,redirect,url_for,flash,session,abort
from flask_bootstrap import Bootstrap
from modelo.Dao import db,Usuario,Vehiculo
from flask_login import login_required,login_user,logout_user,current_user,LoginManager
import json
app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://aguazero:aguazero@localhost/aguazero'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='Cl4v3'

#Implementación de la gestion de usuarios con flask-login
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='mostrar_login'
login_manager.login_message='¡ Tu sesión expiró !'
login_manager.login_message_category="info"
#Implementación de la gestion de usuarios con flask-login
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='mostrar_login'
login_manager.login_message='¡ Tu sesión expiró !'
login_manager.login_message_category="info"

@app.before_request
def before_request():
    session.permanent=True
    #app.permanent_session_lifetime=timedelta(minutes=10)

@app.route("/")
def inicio():
    return render_template('principal.html')

#Inicio del CRUD de usuarios
@app.route('/Usuarios/iniciarSesion')
def mostrar_login():
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))
    else:
        return render_template('usuarios/login.html')

@login_manager.user_loader
def cargar_usuario(id):
    return Usuario.query.get(int(id))

@app.route('/Usuarios/nuevo')
def nuevoUsuario():
    if current_user.is_authenticated and not current_user.is_admin():
        abort(404)
    else:
        return render_template('usuarios/nuevoUsuario.html')

@app.route('/Usuarios/agregar',methods=['post'])
def agregarUsuario():
    try:
        usuario = Usuario()
        usuario.nombre = request.form['nombre']
        usuario.correo = request.form['email']
        usuario.password = request.form['password']
        usuario.tipo = request.form['tipo']
        usuario.estatus = '1'
        usuario.agregar()
        flash('¡ Usuario registrado con éxito !')
    except:
        flash('¡ Error al agregar al usuario !')
    return render_template('usuarios/nuevoUsuario.html')

@app.route("/Usuarios/validarSesion",methods=['POST'])
def login():
    if not current_user.is_authenticated:
        correo = request.form['correo']
        password = request.form['password']
        usuario = Usuario()
        user = usuario.validar(correo, password)
        if user != None:
            login_user(user)
            if current_user.is_active():
                return redirect(url_for('inicio'))
            else:
                logout_user()
                flash('Cuenta inactiva')
                return redirect(url_for('mostrar_login'))
        else:
            flash('Nombre de usuario o contraseña incorrectos')
            return render_template('usuarios/login.html')
    else:
        abort(404)

@app.route('/Usuarios/cerrarSesion')
@login_required
def cerrarSesion():
    logout_user()
    return redirect(url_for('mostrar_login'))

@app.route('/Usuarios/verPerfil')
@login_required
def verPerfil():
    return render_template('usuarios/verPerfil.html')

@app.route('/Usuarios/editarPerfil',methods=['POST'])
@login_required
def editarPerfil():
    try:
        usuario = Usuario()
        usuario.idUsuario = request.form['ID']
        usuario.nombre = request.form['nombre']
        usuario.correo = request.form['email']
        if request.form['password'] != '':
            usuario.password = request.form['password']

        usuario.tipo = request.form['tipo']
        if request.form['bandera'] == 'admin':
            usuario.estatus = request.form['estatus']
        else:
            usuario.estatus = '1'
        usuario.editar()
        flash('¡ Usuario modificado con exito !')
    except:
        flash('¡ Error al modificar al usuario !')
    if request.form['bandera'] == 'admin':
        return redirect(url_for('verUsuarios'))
    else:
        return redirect(url_for('verPerfil'))

@app.route('/Usuarios/eliminar/<int:id>')
@login_required
def eliminarPerfil(id):
    if current_user.is_authenticated and current_user.idUsuario == id:
        try:
            usuario = Usuario()
            usuario.eliminacionLogica(id)
            logout_user()
            flash('Usuario eliminado con exito')
        except:
            flash('Error al eliminar el usuario')
        return redirect(url_for('mostrar_login'))
    else:
        abort(404)

@app.route('/Usuarios/verUsuarios')
@login_required
def verUsuarios():
    if current_user.is_admin():
        usuarios = Usuario()
        return render_template('usuarios/verUsuarios.html', usuarios=usuarios.consultaGeneral())
    else:
        abort(404)

@app.route('/Usuarios/<int:id>')
@login_required
def usuarioIndividual(id):
    if current_user.is_admin():
        usuario = Usuario()
        return render_template('usuarios/verUsuario.html',usuario=usuario.consultaIndividual(id))
    else:
        abort(404)

#Fin del CRUD de usuarios

#error
@app.errorhandler(404)
def error_404(e):
    return render_template("comunes/error_404.html"),404

@app.errorhandler(405)
def error_405(e):
    return render_template("comunes/error_405.html"),405

@app.route('/vehiculo/agregar')
def agregarvehiculo():
    return render_template('vehiculo/nuevo.html')

@app.route('/vehiculo/consultar')
def consultarVehiculos():
    try:
        v = Vehiculo()
    except:
        print("Ocurrio un error")
    return render_template('vehiculo/consultar.html', vehiculo = v.consultaGeneral())

@app.route('/vehiculo/agregandoVehiculo', methods=['post'])
def agregandoVehiculo():
    v = Vehiculo()
    v.placas = request.form['placas']
    v.tipo_de_vehiculo = request.form['tipoVehiculo']
    v.tipo_combustible = request.form['tipoCombustible']
    v.capacidad_tanque = request.form['capacidadTanque']
    v.modelo = request.form['modelo']
    v.año = request.form['año']
    v.capacidad_garrafones = request.form['capacidadGarrafones']
    v.insertar()
    return redirect(url_for('consultarVehiculos'))
@app.route('/vehiculo/actualizandoVehiculo', methods=['post'])
def actualizandoVehiculo():
    v = Vehiculo()
    v.idVehiculo = request.form['idVehiculo']
    v.placas = request.form['placas']
    v.tipo_de_vehiculo = request.form['tipoVehiculo']
    v.tipo_combustible = request.form['tipoCombustible']
    v.capacidad_tanque = request.form['capacidadTanque']
    v.modelo = request.form['modelo']
    v.año = request.form['año']
    v.capacidad_garrafones = request.form['capacidadGarrafones']
    v.actualizar()
    return redirect(url_for('consultarVehiculos'))

@app.route("/vehiculos/consultar/<int:id>")
def consultarVehiculoInd(id):
    v = Vehiculo()
    return render_template('vehiculo/consultaIndividual.html', vehiculo=v.consultaIndividual(id))

@app.route("/vehiculos/eliminar/<int:id>")
def eliminarVehiculo(id):
    v = Vehiculo()
    v.eliminar(id)
    return redirect(url_for('consultarVehiculos'))




if __name__=='__main__':
    db.init_app(app)#Inicializar la BD - pasar la configuración de la url de la BD
    app.run(debug=True)