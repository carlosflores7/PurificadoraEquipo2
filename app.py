import datetime
from datetime import timedelta

from flask import Flask,render_template,request,redirect,url_for,flash,session,abort
from flask_bootstrap import Bootstrap
from modelo.Dao import db,Usuario,Vehiculo,Garrafones,Promociones,Empleado,Tarjetas
from flask_login import login_required,login_user,logout_user,current_user,LoginManager
import json

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Hola.123@localhost/aguazero'
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
    if current_user.is_authenticated and current_user.is_admin():
        return render_template('usuarios/nuevoUsuario.html')
    else:
        abort(404)

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

@app.route('/Usuarios/verUsuarios', methods=['get'])
@login_required
def verUsuarios():
    if current_user.is_admin():
        usuarios = Usuario()
        if request.args.get('tipo') == None:
            if request.args.get('nombre'):
                return render_template('usuarios/verUsuarios.html', usuarios=usuarios.consultaNombre(request.args.get('nombre')),consulta='general')
            else:
                return render_template('usuarios/verUsuarios.html', usuarios=usuarios.consultaGeneral(),consulta='general')
        else:
            return render_template('usuarios/verUsuarios.html', usuarios=usuarios.consultaTipo(request.args.get('tipo')), consulta=request.args.get('tipo'))
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

@app.route('/Usuarios/Pagina/<int:pagina>')
@login_required
def usuariosPagina(pagina):
    if current_user.is_admin():
        usuarios = Usuario()
        return render_template('usuarios/verUsuariosPagina.html', usuarios=usuarios.paginar(pagina),pagina=pagina)
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

#@app.route('/vehiculo/consultar')
#def consultarVehiculos():
#    try:
#        v = Vehiculo()
#    except:
#        print("Ocurrio un error")
#    return render_template('vehiculo/consultar.html', vehiculo = v.consultaGeneral())

@app.route('/vehiculo/consultar/<int:pagina>')
@login_required
def consultarVehiculos(pagina):
    if current_user.is_admin():
        v = Vehiculo()
        if request.args.get('filtro'):
            return render_template('vehiculo/consultarfiltro.html',vehiculo_sin_paginacion=v.filtrar(request.args.get('filtro')), pagina = pagina)
        else:
            return render_template('vehiculo/consultar.html', vehiculo = v.paginar(pagina), pagina = pagina)
    else:
        abort(404)



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
    flash('¡ El vehiculo se ha registrado !')
    return redirect(url_for('agregarvehiculo'))

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

@app.route('/vehiculos/placas/<string:placas>', methods=['Get'])
def consultarPlacas(placas):
    v = Vehiculo()
    return json.dumps(v.consultarPlacas(placas))

#Fin del CRUD Vehiculo

#Inicio del CRUD Garrafones
@app.route('/Garrafones/agregar')
def agregarGarrafones():
    return render_template('/Garrafones/nuevoGarrafon.html')

@app.route('/Garrafones/mostrar/<int:pagina>')
def mostrarGarrafones(pagina):
    garrafon=Garrafones()
    if request.args.get('filtro'):
        return render_template('garrafones/verFiltro.html', garrafon_sin_paginacion=garrafon.filtro(request.args.get('filtro')), pagina=pagina)
    else:
        return render_template('garrafones/verGarrafon.html',g=garrafon.paginacion(pagina),pagina=pagina)

@app.route('/Garrafones/agregando', methods=['post'])
def agregandoGarrafones():

        garrafon = Garrafones()
        garrafon.Estado = request.form['estado']
        garrafon.codigo = request.form['codigo']
        garrafon.capaciodad = request.form['capacidad']
        garrafon.precio_retornable = request.form['precio_retornable']
        garrafon.precio_completo = request.form['precio_completo']
        garrafon.insertar()
        flash('¡ El garrafon se ha registrado !')

        return redirect(url_for("agregarGarrafones"))

#@app.route('/Garrafones/mostrar')
#def mostrarGarrafones():
 #       garrafon = Garrafones()
  #      return render_template('Garrafones/verGarrafon.html', g = garrafon.consultaGeneral())

@app.route('/Garrafones/actualizando', methods=['post'])
def actualizandoGarrafones():

        garrafon = Garrafones()
        garrafon.idGarrafon = request.form['idGarrafon']
        garrafon.Estado = request.form['estado']
        garrafon.codigo = request.form['codigo']
        garrafon.capaciodad = request.form['capacidad']
        garrafon.precio_retornable = request.form['precioRetornable']
        garrafon.precio_completo = request.form['precioCompleto']
        garrafon.actualizar()
        return redirect(url_for("inicio"))

@app.route("/Garrafones/mostrarIndividual/<int:id>")
def consultarGarrafonesIndividual(id):
    garrafon = Garrafones()
    return render_template('Garrafones/actualizarGarrafon.html', g = garrafon.consultaIndividual(id))

@app.route("/Garrafones/eliminar/<int:id>")
def eliminarGarrafon(id):
    garrafon = Garrafones()
    garrafon.eliminar(id)
    return redirect(url_for("inicio"))


#Fin del CRUD Garrafones

#Inicio del Crud de Promociones
@app.route('/Promociones/agregar')
def agregarPromocion():
    return render_template('/Promociones/nuevaPromocion.html')

@app.route('/Promociones/agregando', methods=['post'])
def agregarPromociones():
    promocion = Promociones()
    promocion.cantidad_max = request.form['cantidadMaxima']
    promocion.cantidad_min = request.form['cantidadMinima']
    promocion.estatus = request.form['estatus']
    promocion.porcentaje = request.form['porcentaje']
    promocion.insertar()
    flash('¡La promocion se ha agregado!')

    return redirect(url_for("agregarPromocion"))

@app.route('/Promociones/pagina/<int:pagina>')
def consultarPromociones(pagina):
    promociones=Promociones()
    return render_template('promociones/consultar.html',promociones=promociones.paginacion(pagina),pagina=pagina)

@app.route('/Promociones/<int:id>')
def promocionesIndividual(id):
    promociones=Promociones()
    return render_template('promociones/consultaIndividual.html',promociones=promociones.consultaIndividual(id))


@app.route('/Promociones/actualizar', methods=['post'])
def actualizarPromociones():
    promocion = Promociones()
    promocion.idpromocion = request.form['ID']
    promocion.cantidad_max = request.form['cantidadMaxima']
    promocion.cantidad_min = request.form['cantidadMinima']
    promocion.estatus = request.form['estatus']
    promocion.porcentaje = request.form['porcentaje']
    promocion.actualizar()
    flash('¡La promocion se ha actualizado''!')

    return redirect(url_for("inicio"))

@app.route('/Promociones/eliminar/<int:id>')
def eliminarPromocion(id):
    try:
        promocion=Promociones()
        promocion.eliminacionLogica(id)
        flash('¡La promocion se ha eliminado''!')
    except:
        flash('¡ERROR''!')
    return redirect(url_for("inicio"))
#Fin del CRUD PROMOCIONES

#CRUD TARJETAS
@app.route('/Tarjetas/agregar')
def agregarTarjeta():
    e = Empleado()
    return render_template('/tarjetas/nueva.html', empleado = e.consultaGeneral())

@app.route('/Tarjetas/consultar')
def consultarTarjetas():
    t = Tarjetas()
    return render_template('/tarjetas/consulta.html', tarjetas = t.consultaGeneral())

@app.route('/Tarjetas/editar/<int:id>')
def editarTarjeta(id):
    t = Tarjetas()
    e = Empleado()
    u = Usuario()
    tar = t.consultaIndividual(id)
    emp = tar.Empleado_idEmpleado
    empleado = e.consultaIndividual(emp)
    usu = empleado.Usuarios_idUsuario
    return render_template('/tarjetas/consultarIndividual.html',tarjeta = t.consultaIndividual(id), usuario = u.consultaIndividual(usu))

@app.route('/Tarjetas/agregandoTarjeta', methods=['post'])
def agregandoTarjeta():
    try:
        t = Tarjetas()
        t.Empleado_idEmpleado = request.form['empleado']
        t.numero_tarjeta = request.form['numero']
        t.banco = request.form['banco']
        t.insertar()
        flash('¡La tarjeta se ha agregado!')
    except:
        flash('Fallo al guardar la tarjeta')
    return redirect(url_for('agregarTarjeta'))

@app.route('/Tarjetas/editandoTarjeta', methods=['post'])
def editandoTarjeta():
    t = Tarjetas()
    t.idTarjeta=request.form['idTarjeta']
    t.Empleado_idEmpleado = request.form['idEmpleado']
    t.numero_tarjeta = request.form['numero']
    t.banco = request.form['banco']
    t.actualizar()
    flash('¡La tarjeta se actualizo!')
    return redirect(url_for('consultarTarjetas'))


@app.route("/Tarjetas/eliminar/<int:id>")
def eliminarTarjetas(id):
    t = Tarjetas()
    t.eliminar(id)
    flash('¡La tarjeta se elimino!')
    return redirect(url_for('consultarTarjetas'))

#FIN DEL CRUD TARJETAS

if __name__=='__main__':
    db.init_app(app)#Inicializar la BD - pasar la configuración de la url de la BD
    app.run(debug=True)