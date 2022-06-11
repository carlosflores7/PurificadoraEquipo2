import datetime
import io
from datetime import timedelta

import xlwt
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, make_response, Response
from flask_bootstrap import Bootstrap
import pdfkit
from modelo.Dao import db,Usuario,Vehiculo,Garrafones,Promociones,Empleado,Tarjetas,Puesto,Repartidor, VentasDetalle, Ventas,Factura,Cliente,Pedidos, Nomina,Pagos,Prestamos,Promociones_Venta
from flask_login import login_required,login_user,logout_user,current_user,LoginManager
import json
from datetime import date
app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost/aguazero'
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
    ##if current_user.is_authenticated and current_user.is_admin():
        return render_template('usuarios/nuevoUsuario.html')
    ##else:
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
    promocion.estatus = request.form['estatus']
    promocion.porcentaje = request.form['porcentaje']
    promocion.porcentaje = request.form['codigo']
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


@app.route('/Tarjetas/consultar/<int:pagina>')
@login_required
def consultarTarjetas(pagina):
    if current_user.is_admin():
        t = Tarjetas()
        if request.args.get('filtro'):
            return render_template('tarjetas/consultarfiltro.html',tarjeta_sin_paginacion=t.filtrar(request.args.get('filtro')), pagina = pagina)
        else:
            return render_template('tarjetas/consulta.html', tarjetas = t.paginar(pagina), pagina = pagina)
    else:
        abort(404)
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
    return redirect(url_for('consultarTarjetas', pagina=1))

@app.route('/Tarjetas/editandoTarjeta', methods=['post'])
def editandoTarjeta():
    t = Tarjetas()
    t.idTarjeta=request.form['idTarjeta']
    t.Empleado_idEmpleado = request.form['idEmpleado']
    t.numero_tarjeta = request.form['numero']
    t.banco = request.form['banco']
    t.actualizar()
    flash('¡La tarjeta se actualizo!')
    return redirect(url_for('consultarTarjetas', pagina=1))


@app.route("/Tarjetas/eliminar/<int:id>")
def eliminarTarjetas(id):
    t = Tarjetas()
    t.eliminar(id)
    flash('¡La tarjeta se elimino!')
    return redirect(url_for('consultarTarjetas', pagina=1))

#FIN DEL CRUD TARJETAS

#INICIA CRUD DE EMPLEADOS

@app.route("/Empleados/nuevo")
def nuevoEmpleado():
    usuarios = Usuario()
    puestos = Puesto()
    return render_template('empleados/nuevoEmpleado.html', usuarios = usuarios.consultaTipo('Empleado'), puestos=puestos.consultaGeneral())

@app.route('/Empleados/agregar',methods=['post'])
def agregarEmpleado():
    try:
        empleado = Empleado()
        empleado.tipoEmpleado = 'A'
        empleado.turno = request.form['turno']
        empleado.nss = request.form['nss']
        empleado.Usuarios_idUsuario = request.form['usuario']
        empleado.puestos_idPuesto = request.form['puesto']
        empleado.insertar()
        flash('¡ Empleado registrado con éxito !')
    except:
        flash('¡ Error al agregar al empleado !')
    return redirect(url_for('nuevoEmpleado'))

@app.route('/Empleados/Pagina/<int:pagina>')
def consultarEmpleados(pagina):
    empleados = Empleado()
    return render_template('/empleados/consultaGeneral.html', empleados = empleados.paginar(pagina), pagina=pagina)

@app.route('/Empleados/verEmpleados')
def verEmpleados():
    empleados = Empleado()
    tipo = request.args.get('tipo')
    if request.args.get('nombre') == None:
        return render_template('/empleados/consulta2.html', empleados = empleados.consultaGeneral(), tipo=tipo)
    else:
        return render_template('/empleados/consulta2.html', empleados=empleados.consultaGeneral(),nombre=request.args.get('nombre'))

@app.route('/Empleados/<int:id>')
def consultaIndividualEmpleado(id):
    empleados = Empleado()
    puestos = Puesto()
    return render_template('/empleados/consultaIndividual.html', e = empleados.consultaIndividual(id), puestos=puestos.consultaGeneral())

@app.route('/Empleados/editar',methods=['post'])
def editarEmpleado():
    try:
        empleado = Empleado()
        empleado.idEmpleado = request.form['ID']
        empleado.tipoEmpleado = request.form['estatus']
        empleado.turno = request.form['turno']
        empleado.nss = request.form['nss']
        empleado.puestos_idPuesto = request.form['puesto']
        empleado.editar()
        flash('¡ Empleado editado con éxito !')
    except:
        flash('¡ Error al editar al empleado !')
    return redirect(url_for('consultarEmpleados', pagina=1))

@app.route('/Empleados/eliminar/<int:id>')
@login_required
def eliminarEmpleado(id):
    if current_user.is_authenticated and current_user.is_admin():
        try:
            empleado = Empleado()
            empleado.eliminacionLogica(id)
            flash('Empleado eliminado de su puesto')
        except:
            flash('Error al eliminar empleado')
        return redirect(url_for('consultarEmpleados', pagina=1))
    else:
        abort(404)

#TERMINA CRUD DE EMPLEADOS

#INICIA CRUD DE REPARTIDOR
@app.route('/Repartidores/Pagina/<int:pagina>')
@login_required
def consultarRepartidores(pagina):
    repartidores = Repartidor()
    return render_template('/repartidores/consultaGeneral.html', repartidores=repartidores.paginar(pagina),pagina=pagina)

@app.route("/Repartidores/nuevo")
def nuevoRepartidor():
    empleados = Empleado()
    vehiculos = Vehiculo()
    return render_template('repartidores/nuevoRepartidor.html', empleados=empleados.consultaGeneral(),vehiculos=vehiculos.consultaGeneral())

@app.route('/Repartidores/agregar',methods=['post'])
def agregarRepartidor():
    try:
        repartidor = Repartidor()
        repartidor.Empleado_idEmpleado = request.form['empleado']
        repartidor.Vehiculo_idVehiculo = request.form['vehiculo']
        repartidor.ruta = request.form['ruta']
        repartidor.folio_de_licencia = request.form['folio']
        repartidor.insertar()
        flash('¡ Repartidor registrado con éxito !')
    except:
        flash('¡ Error al agregar al repartidor !')
    return redirect(url_for('nuevoRepartidor'))

@app.route('/Repartidores/<int:id>')
@login_required
def verRepartidorIndividual(id):
    repartidores = Repartidor()
    vehiculos = Vehiculo()
    return render_template('/repartidores/consultaIndividual.html', r=repartidores.consultaIndividual(id), vehiculos=vehiculos.consultaGeneral())

@app.route('/Repartidores/editar',methods=['post'])
def editarRepartidor():
    try:
        repartidor = Repartidor()
        repartidor.idRepartidor = request.form['ID']
        repartidor.Empleado_idEmpleado = request.form['empleado']
        repartidor.Vehiculo_idVehiculo = request.form['vehiculo']
        repartidor.ruta = request.form['ruta']
        repartidor.folio_de_licencia = request.form['folio']
        repartidor.actualizar()
        flash('¡ Repartidor actualizado con éxito !')
    except:
        flash('¡ Error al actualizar al repartidor !')
    return redirect(url_for('consultarRepartidores', pagina=1))

@app.route('/Repartidores/eliminar/<int:id>')
@login_required
def eliminarRepartidor(id):
    if current_user.is_authenticated and current_user.is_admin():
        try:
            repartidor = Repartidor()
            repartidor.eliminar(id)
            flash('Repartidor eliminado con éxito')
        except:
            flash('Error al eliminar al repartidor')
        return redirect(url_for('consultarRepartidores', pagina=1))
    else:
        abort(404)

#FIN CRUD DE REPARTIDOR

##Inicio del CRUD Ventas_detalle

@app.route('/Ventas_detalle/agregar')
def agregarVentas_detalle():
    garrafones = Garrafones()
    ventas = Ventas()
    return render_template('/Ventas_detalle/nuevaVenta_detalle.html', garrafones = garrafones.consultaGeneral(), ventas = ventas.consultaGeneral())

@app.route('/Ventas_detalle/agregando', methods=['post'])
def agregandoVentasDetalle():

        dventas = VentasDetalle()

        dventas.Garrafones_idGarrafon = request.form['garrafones']
        dventas.cantidad = request.form['cantidad']
        dventas.precio_venta = request.form['PrecioVenta']
        dventas.prestado = request.form['prestado']
        dventas.Ventas_idVenta = request.form['ventas']
        dventas.insertar()

        flash('¡ El detalle de la venta se ha registrado !')

        return redirect(url_for("agregarVentas_detalle"))

@app.route('/Ventas_detalle/mostrar/<int:pagina>')
def mostrarVentasDetalle(pagina):
    dventas = VentasDetalle()
    if request.args.get('filtro'):
        return render_template('Ventas_detalle/verFiltro_Ventas_detalle.html', dventas_sin_paginacion=dventas.filtro(request.args.get('filtro')), pagina=pagina)
    else:
        return render_template('Ventas_detalle/verVentas_detalles.html', dventas=dventas.paginacion(pagina), pagina=pagina)


@app.route('/Ventas_detalle/actualizando', methods=['post'])
def actualizandoVentas_detalle():
         dventas = VentasDetalle()

         dventas.idventas_detalle = request.form['id']
         dventas.cantidad = request.form['cantidad']
         dventas.precio_venta = request.form['precio_venta']
         dventas.prestado = request.form['prestado']
         dventas.actualizar()
         return redirect(url_for("inicio"))

@app.route("/Ventas_detalle/mostrarIndividual/<int:id>")
def consultarVentas_DetalleIndividual(id):
    dventas = VentasDetalle()
    return render_template('Ventas_detalle/actualizarVenta_detalle.html', dventa = dventas.consultaIndividual(id))

@app.route("/Ventas_detalle/eliminar/<int:id>")
def eliminarVentas_detalle(id):
    dventas = VentasDetalle()
    dventas.eliminar(id)
    return redirect(url_for("inicio"))
##Fin del CRUD

##Inicio del CRUD FACTURAS

#NUEVA FACTURA
@app.route('/Factura/nueva')
def agregarFactura():
    if current_user.is_Cliente():
        c = Cliente()
        ventas = Ventas()
        id = current_user.idUsuario
        aux = c.consulta(id)
        print(aux.idCliente)
        return render_template('/Factura/NuevoFactura.html', ventas = ventas.ventasCliente(aux.idCliente))
    if current_user.is_admin():
        c = Cliente ()
        v = Ventas ()
        return render_template('/Factura/nuevaFacturaAdmin.html', cliente = c.consultaGeneral(), ventas = v.consultaGeneral())
    else:
        abort(404)


@app.route('/Factura/agregando', methods=['post'])
def agregarFacturas():
    if current_user.is_Cliente():
        fac = Factura()
        c = Cliente()
        idAux=current_user.idUsuario
        aux = c.consulta(idAux)
        fac.fecha = request.form['Fecha']
        fac.Cliente_idCliente = aux.idCliente
        fac.Ventas_idVenta = request.form['Ventas']
        fac.insertar()
        flash('¡La factura se ha registrado!')

        return redirect(url_for("agregarFactura"))
    if current_user.is_admin():
        f = Factura()
        f.fecha = request.form['Fecha']
        f.Cliente_idCliente = request.form['Clientes']
        f.Ventas_idVenta = request.form['Ventas']
        f.insertar()
        flash('¡La factura se ha registrado!')

        return redirect(url_for("agregarFactura"))
    else:
        abort(404)

#MOSTRAR
@app.route('/Factura/consultar/<int:pagina>')
@login_required
def consultarFactura(pagina):
    if current_user.is_admin() :
        fac = Factura()
        if request.args.get('filtro'):
            return render_template('Factura/ConsultarFiltro.html', factura_sin_paginacion = fac.filtrar(request.args.get('filtro')), pagina = pagina)
        else:
                return render_template('Factura/ConsultarFactura.html', factura = fac.paginar(pagina), pagina = pagina)
    elif current_user.is_Cliente():
        fac = Factura()
        c = Cliente()
        v = Ventas()
        id = current_user.idUsuario
        aux = c.consulta(id)
        facturas = fac.facturasCliente(aux.idCliente)
        return render_template('Factura/facturasCliente.html', factura=facturas)

    else:
        abort(404)


#EDITAR
@app.route('/Factura/editar/<int:id>')
def editarFactura(id):
    fac = Factura()
    c = Cliente()
    u = Usuario()
    f = fac.consultaIndividual(id)
    cli = f.Cliente_idCliente
    cliente = c.consultaIndividual(cli)
    usu = cliente.Usuarios_idUsuario
    return render_template('/Factura/ConsultarIndividual.html', fac=fac.consultaIndividual(id), usuario = u.consultaIndividual(usu))

@app.route('/Factura/editandoFactura', methods=['post'])
def editandoFactura():
    fac = Factura()
    fac.idfactura=request.form['idfactura']
    fac.fecha = request.form['fecha']
    fac.Cliente_idCliente = request.form['Cliente']
    fac.Ventas_idVenta = request.form['Ventas']
    fac.actualizar()
    flash('¡La factura se actualizó!')
    return redirect(url_for('consultarFactura', pagina=1))

#Eliminar
@app.route("/Factura/eliminar/<int:id>")
def eliminarFactura(id):
    fac = Factura()
    fac.eliminar(id)
    flash('¡La Factura se elimino!')
    return redirect(url_for('consultarFactura', pagina=1))
##Fin del CRUD FACTURAS


@app.route("/Pedido/Nuevo")
def nuevoPedido():
    c = Cliente()
    u = Usuario()
    if current_user.is_Cliente():
        id = current_user.idUsuario
        aux = c.consulta(id)
        usuario = u.consultaIndividual(id)
        return render_template("/pedidos/nuevoPedido.html", cliente = aux.idCliente, usuario = usuario)
    if current_user.is_admin() or current_user.is_Empleado():
        return render_template("/pedidos/nuevoPedidoCliAdmi.html", clientes = c.consultaGeneral())
    else:
        abort(404)

@app.route("/Pedido/Agregando", methods=['post'])
def reglaNegocio():
    p = Pedidos()
    pro = Promociones()
    codigoPromocion = request.form['codigoPromocion']
    idCliente = request.form['idCliente']
    garrafones = request.form['cGarrafones']
    p.cantidad_garrafones = garrafones;
    p.ClienteID = idCliente
    gPrestados = request.form['gprestados']
    if gPrestados == '1':
        cGarrafones = request.form['cGarrafonesPrestados']
    else:
        cGarrafones = 0
    print(gPrestados)
    resultCodigo = pro.consultaCodigo(codigoPromocion)
    if resultCodigo != None:
        p.insertar()
        garrafonesInt = int(garrafones)
        precio = (garrafonesInt * 20)
        precioaux = float(precio)#200
        descuento = (precioaux * resultCodigo.porcentaje)/100 #20
        precioTotal = (precioaux - descuento)
        p.procedimientAlmacenado(codigoPromocion,p.idPedido,precioTotal,idCliente, cGarrafones)
        flash('El pedido esta en camino y se le aplico una promoción')
        return redirect(url_for("nuevoPedido"))
    else:
        p.insertar()
        garrafonesInt = int(garrafones)
        precioTotal = garrafonesInt*20
        p.procedimientAlmacenado('00000',p.idPedido, precioTotal,idCliente,cGarrafones)
        flash('El pedido esta en camino, pero no la promocion esta invalida')
        return redirect(url_for("nuevoPedido"))

@app.route("/Pedido/Mispedidos")
def misPedidos():
    if current_user.is_Cliente():
        c = Cliente()
        v = Ventas()
        id = current_user.idUsuario
        aux = c.consulta(id)
        pedidos = v.consultarMisPedidos(aux.idCliente)
        return render_template("/pedidos/misPedidos.html", p = pedidos)
    elif current_user.is_admin():
        v = Ventas()
        return render_template("/pedidos/consultarPedidosAdmin.html", p = v.consultaGeneral())
    elif current_user.is_Empleado():
        v = Ventas()
        return render_template("/pedidos/consultarPedidosRepartidor.html", p = v.consultaGeneral())
    else:
        abort(404)
@app.route("/Pedido/Confirmar/<int:id>")
def confirmarPedido(id):
    if current_user.is_Cliente():
       v = Ventas()
       v.idVenta = id
       v.estatus = "Entregado"
       v.actualizar()
       flash('La venta se a entregado')
       return redirect(url_for("misPedidos"))
    else:
        abort(404)
@app.route("/Pedido/Cancelar/<int:id>")
def cancelarPedido(id):
    if current_user.is_Cliente():
       v = Ventas()
       v.idVenta = id
       v.estatus = "Cancelado"
       v.actualizar()
       flash('La venta se a cancelado')
       return redirect(url_for("misPedidos"))
    else:
        abort(404)

#CRUD de clientes#

@app.route("/Cliente/nuevo")
def nuevoCliente():
    return render_template('clientes/agregarCliente.html')

@app.route("/Cliente/agregando", methods=['post'])
def agregandoCliente():
    try:
        usuario = Usuario()
        usuario.nombre = request.form['nombre']
        usuario.correo = request.form['email']
        usuario.password = request.form['password']
        usuario.tipo = 'Cliente'
        usuario.estatus = '1'
        usuario.agregar()
        cliente = Cliente()
        cliente.domicilio = request.form['domicilio']
        cliente.localidad = request.form['localidad']
        cliente.rfc = request.form['rfc']
        cliente.Usuarios_idUsuario = usuario.idUsuario
        cliente.insertar()
        flash('¡ Cliente registrado con éxito !')
    except:
        flash('¡ Error al agregar al cliente !')
    return redirect(url_for('nuevoCliente'))

@app.route("/Cliente/consultar/<int:pagina>")
def verClientes(pagina):
    clientes = Cliente()
    return render_template('clientes/consultaGeneral.html', clientes=clientes.paginacion(pagina), pagina=pagina)

@app.route("/Cliente/ind/<int:id>")
def verClienteIndividual(id):
    cliente = Cliente()
    return render_template('clientes/verCliente.html', c=cliente.consultaIndividual(id))

@app.route("/Cliente/actualizar", methods=['post'])
def editandoCliente():
    try:
        usuario = Usuario()
        usuario.idUsuario = request.form['IDUSUARIO']
        usuario.nombre = request.form['nombre']
        usuario.correo = request.form['email']
        if request.form['password'] != '':
            usuario.password = request.form['password']
        usuario.editar()
        cliente = Cliente()
        cliente.idCliente = request.form['IDCLIENTE']
        cliente.domicilio = request.form['domicilio']
        cliente.localidad = request.form['localidad']
        cliente.rfc = request.form['rfc']
        cliente.Usuarios_idUsuario = usuario.idUsuario
        cliente.actualizar()
        flash('¡ Cliente editado con éxito !')
    except:
        flash('¡ Error al editar al cliente !')
    return redirect(url_for('verClienteIndividual', id=request.form['IDCLIENTE']))

@app.route('/Cliente/eliminar/<int:id>')
def eliminarCliente(id):
    if current_user.is_authenticated:
        try:
            usuario = Usuario()
            usuario.eliminacionLogica(id)
            if current_user.idUsuario == id:
                logout_user()
            flash('Usuario eliminado con exito')
        except:
            flash('Error al eliminar el usuario')
        return redirect(url_for('inicio'))
    else:
        abort(404)

@app.route('/Cliente/activar/<int:id>')
def activarCliente(id):
    if current_user.is_authenticated:
        try:
            usuario = Usuario()
            usuario = usuario.consultaIndividual(id)
            usuario.estatus=1
            usuario.editar()
            flash('Usuario activado con exito')
        except:
            flash('Error al activar el usuario')
        return redirect(url_for('inicio'))
    else:
        abort(404)

@app.route('/PDF/nuevo/<int:id>')
def pdf_template(id):
    f = Factura()
    factura = f.consultaIndividual(id)

    rendered = render_template('PDF/format.html', fa = factura, today = date.today())
    config = pdfkit.configuration(wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdf = pdfkit.from_string(rendered, False, configuration= config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename= output.pdf'

    return response
@app.route('/Excel/Download')
def downloadExcel():
    if current_user.is_authenticated and current_user.is_admin():
        v = Ventas()
        ventas = v.consultaGeneral()
        output  = io.BytesIO()
        workbook = xlwt.Workbook()
        sh = workbook.add_sheet('Ventas')
        sh.write(0, 0, 'Folio de Venta')
        sh.write(0, 1, 'Precio_Total')
        sh.write(0, 2, 'Fecha')
        sh.write(0, 3, 'Estatus')
        sh.write(0, 4, 'Codigo de Promocion')
        sh.write(0, 5, 'Nombre del Repartidor')
        sh.write(0, 6, 'Nombre del Cliente')
        sh.write(0, 7, 'Folio de Pedido')
        sh.write(0, 8, 'Cantidad de garrafones')

        idx = 0
        for v in ventas:
            sh.write(idx + 1, 0, str(v.idVenta))
            sh.write(idx + 1, 1, str(v.precio_total))
            sh.write(idx + 1, 2, str(v.fecha))
            sh.write(idx + 1, 3, str(v.estatus))
            if v.promociones.codigo == '00000':
                sh.write(idx + 1, 4, str("No aplica"))
            else:
                sh.write(idx + 1, 4, str(v.promociones.codigo))

            sh.write(idx + 1, 5, str(v.repartidor.empleado.usuario.nombre))
            sh.write(idx + 1, 6, str(v.cliente.usuario.nombre))
            sh.write(idx + 1, 7, str(v.idPedido))
            sh.write(idx + 1, 8, str(v.pe.cantidad_garrafones))

            idx +=1
        workbook.save(output)
        output.seek(0)

        return Response(output, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=Ventas.xls"})
    else:
        abort(404)

#@app.route("/venta/consultar")
#def consultarVentas():
#    if current_user.is_authenticated and current_user.is_admin():
#        v = Ventas()
#        return render_template('ventas/consultarVentas.html', ventas = v.consultaGeneral())
#    else:
#        abort(404)

@app.route("/Nomina/nueva")
def nuevaNomina():
    if current_user.is_authenticated and current_user.is_admin():
        e = Empleado()
        return render_template('nominas/nuevaNomina.html', empleado = e.consultaGeneral())
    else:
        abort(404)

@app.route("/Nomina/agregar", methods=['post'])
def agregarNomina():
    if current_user.is_authenticated and current_user.is_admin():
        try:
            n = Nomina()
            e = Empleado()
            dias = int(request.form['dias_trabajados'])
            empleado = request.form['empleado']

            mensaje = ""
            if empleado == "opcion":
                mensaje += "Empleado incorrecto\n"

            empleadoaux = e.consultaIndividual(empleado)
            if mensaje == "":
                n.Empleado_idEmpleado = empleado
                d = empleadoaux.puesto.salario * dias
                n.salario_total =d

                print(d)
                n.dias_trabajados = dias
                n.insertar()
                flash("Nomina registrada")
            else:
                flash(mensaje)
        except:
            flash("Nomina ya registrada")
    else:
        abort(404)
    return redirect(url_for('nuevaNomina'))
@app.route("/Nomina/consultar/<int:pagina>")
@login_required
def consultarNomina(pagina):
    if current_user.is_authenticated and current_user.is_admin():
        n = Nomina()
        e = Empleado()
        return render_template('nominas/consultarNominas.html', nomina=n.paginar(pagina), pagina=pagina, empleado = e.consultaGeneral())
    else:
        abort(404)
@app.route("/Nomina/<int:id>")
@login_required
def editarNomina(id):
    if current_user.is_authenticated and current_user.is_admin():
        n = Nomina()
        return render_template('nominas/verNomina.html', nomina = n.consultaIndividual(id))
    else:
        abort(404)

@app.route("/Nomina/actualizar", methods=['post'])
@login_required
def actualizarNomina():
    if current_user.is_authenticated and current_user.is_admin():
        n = Nomina()
        e = Empleado()
        e = e.consultaIndividual(request.form['idEmpleado'])
        dias = int(request.form['dias_trabajados'])
        mensaje = ""

        if mensaje == "":
            n.idnomina = request.form['idNomina']
            n.salario_total = e.puesto.salario * dias
            n.dias_trabajados = dias
            n.actualizar()
            flash("Nomina actualizada")
        else:
            flash(mensaje)
    else:
        abort(404)
    return redirect("/Nomina/consultar/1")
@app.route("/Nomina/eliminar/<int:id>")
def eliminarNomina(id):
    if current_user.is_authenticated and current_user.is_admin():
        try:
            n = Nomina()
            n.eliminar(id)
            flash("Nomina eliminada")
        except:
            flash("Error al eliminar la nomina")

    else:
        abort(404)

    return redirect("/Nomina/consultar/1")
@app.route('/Pago/nuevo')
def nuevoPago():
    #if current_user.is_authenticated and current_user.is_admin():
    return render_template('pagos/nuevoPago.html')
    #else:
        #abort(404)

#Fin CRUD de clientes#

#Inicio CRUD Prestamos
@app.route('/Prestamos/nuevo')
def agregarPrestamo():
    cliente = Cliente()
    ventas = Ventas()
    garrafones = Garrafones()
    empleado = Empleado()

    return render_template('/Prestamos/NuevoPrestamo.html', cliente = cliente.consultaGeneral(), ventas = ventas.consultaGeneral(), garrafones = garrafones.consultaGeneral() , empleado = empleado.consultaGeneral())



@app.route('/Prestamos/agregando', methods=['post'])
def agregarPrestamos():
    prestamo = Prestamos()
    prestamo.Empleado_idEmpleado = request.form['Empleado']
    prestamo.Ventas_idVentas = request.form['Ventas']
    prestamo.garrafones_prestados = request.form['cGarrafones']
    prestamo.Cliente_idCliente = request.form['Cliente']
    prestamo.insertar()
    flash('¡El prestamo se ha registrado!')

    return redirect(url_for("agregarPrestamo"))

#MOSTRAR
@app.route('/Prestamos/consultar/<int:pagina>')
@login_required
def consultarPrestamos(pagina):
    if current_user.is_admin() or current_user.is_Empleado():
        p = Prestamos()
        if request.args.get('filtro'):
            return render_template('Prestamos/ConsultarFiltro.html', prestamo_sin_paginacion = p.filtrar(request.args.get('filtro')), pagina = pagina)
        else:
                return render_template('Prestamos/ConsultarPrestamo.html', prestamos = p.paginar(pagina), pagina = pagina)
    else:
        abort(404)

@app.route('/Prestamos/editar/<int:id>')
@login_required
def abrirPrestamo(id):
    p = Prestamos()
    return render_template('Prestamos/editarPrestamo.html', prestamo = p.consultaIndividual(id))

@app.route('/Prestamos/editando', methods = ['post'])
@login_required
def actualizandoPrestamo():
    if current_user.is_admin() or current_user.is_Empleado():
        p = Prestamos()
        p.idPrestamos = request.form['id']
        prestados = int(request.form['cGarrafones'])
        entregados = int(request.form['garrafones_entregados'])
        if entregados <= prestados:
            p.garrafones_entregados = entregados
            p.actualizar()
            flash("Se actualizo el prestamo")
        else:
            flash("No se puede actualizar")
        return redirect(url_for('abrirPrestamo', id=p.idPrestamos))
    else:
        abort(404)
#Eliminar
@app.route("/Prestamos/eliminar/<int:id>")
def eliminarPrestamos(id):
    p = Prestamos()
    p.eliminar(id)
    flash('¡Se ha eliminado el prestamo!')
    return redirect(url_for('consultarPrestamos', pagina=1))


#Fin CRUD Prestamos


#Inicio CRUD Pagos
@app.route('/Pagos/nuevo')
def agregarPago():
    nomina = Nomina()
    tarjeta = Tarjetas()

    return render_template('/Pagos/NuevoPagos.html', nomina = nomina.consultaGeneral(), tarjeta = tarjeta.consultaGeneral())

@app.route('/Pagos/agregando', methods=['post'])
def agregarPagos():
    pay = Pagos()
    n = Nomina()

    dias = int(request.form['dias_pe'])

    pay.nominas_idnomina= request.form['idNomina']
    pay.fecha = request.form['Fecha']
    pay.dias_pe = dias
    pay.tarjetas_idTarjeta = request.form['Tarjetas']
    auxpago = n.consultaIndividual(pay.nominas_idnomina)

    if dias != 0:
        descontar = auxpago.empleado.puesto.salario * dias
        pay.total =  auxpago.salario_total - descontar
    else:
        pay.total = auxpago.salario_total

    pay.insertar()
    flash('¡El pago se ha registrado')

    return redirect(url_for("agregarPago"))

#MOSTRAR
@app.route('/Pagos/consultar/<int:pagina>')
@login_required
def consultarPagos(pagina):
    if current_user.is_admin() :
        pay = Pagos()
        if request.args.get('filtro'):
            return render_template('Pagos/ConsultarFiltro.html', pagos_sin_paginacion = pay.filtrar(request.args.get('filtro')), pagina = pagina)
        else:
                return render_template('Pagos/ConsultarPagos.html', pagos = pay.paginar(pagina), pagina = pagina)
    else:
        abort(404)

#EDITAR
@app.route('/Pagos/editar/<int:id>')
def editarPagos(id):
    pay = Pagos()
    n = Nomina()
    t = Tarjetas()
    return render_template('/Pagos/ConsultarIndividual.html', pay=pay.consultaIndividual(id))

@app.route('/Pagos/editandoPagos', methods=['post'])
def editandoPagos():
    pay = Pagos()
    pay.idPago=request.form['Pago']
    pay.nominas_idnomina = request.form['Nomina']
    pay.fecha = request.form['Fecha']
    pay.tarjetas_idTarjeta = request.form['Tarjetas']
    pay.actualizar()
    flash('¡Se actualizó el pago!')
    return redirect(url_for('consultarPagos', pagina=1))

#Eliminar
@app.route("/Pagos/eliminar/<int:id>")
def eliminarPagos(id):
    pay = Pagos()
    pay.eliminar(id)
    flash('¡Se ha eliminado el Pago!')
    return redirect(url_for('consultarPagos', pagina=1))

#Inicia CRUD de Puestos
@app.route("/Puesto/consultar/<int:pagina>")
def verPuestos(pagina):
    puestos = Puesto()
    return render_template('puestos/consultaGeneral.html', puestos=puestos.paginar(pagina), pagina=pagina)

@app.route("/Puesto/nuevo")
def nuevoPuesto():
    return render_template('puestos/agregarPuesto.html')

@app.route("/Puesto/agregando", methods=['post'])
def agregandoPuesto():
    try:
        puesto = Puesto()
        puesto.nombre = request.form['nombre']
        puesto.salario = request.form['salario']
        puesto.descripcion = request.form['descripcion']
        puesto.insertar()

        flash('¡ Puesto registrado con éxito !')
    except:
        flash('¡ Error al agregar un nuevo Puesto !')
    return redirect(url_for('nuevoPuesto'))

@app.route("/Puesto/ind/<int:id>")
def verPuestoIndividual(id):
    puesto = Puesto()
    return render_template('puestos/verPuesto.html', p=puesto.consultaIndividual(id))

@app.route("/Puesto/actualizar", methods=['post'])
def actualizandoPuesto():
    try:
        puesto = Puesto()
        puesto.idPuesto = request.form['ID']
        puesto.nombre = request.form['nombre']
        puesto.salario = request.form['salario']
        puesto.descripcion = request.form['descripcion']
        puesto.editar()

        flash('¡ Puesto editado con éxito !')
    except:
        flash('¡ Error al editar el puesto !')
    return redirect(url_for('verPuestoIndividual', id=request.form['ID']))

@app.route('/Puesto/eliminar/<int:id>')
def eliminarPuesto(id):
    try:
        puesto = Puesto()
        puesto.eliminar(id)
        flash('Puesto eliminado con éxito')
    except:
        flash('Error al eliminar el puesto')
    return redirect(url_for('verPuestos', pagina=1))

#Fin de CRUD de puestos

#Inicio CRUD Promociones Venta
@app.route('/PromocionesVenta/nuevo')
def agregarPromocionVenta():
    promociones = Promociones()
    ventas = Ventas()
    return render_template('/Promociones_Venta/NuevoPromocionVenta.html', promociones = promociones.consultaGeneral(), ventas = ventas.consultaGeneral())



@app.route('/Promociones_Venta/agregando', methods=['post'])
def agregandoPromocionVenta():
    pventas = Promociones_Venta()
    pventas.promociones_idpromocion = request.form['Promociones']
    pventas.Ventas_idVentas = request.form['Ventas']
    pventas.insertar()
    flash('¡La Promocion de la venta se ha registrado!')

    return redirect(url_for("agregarPromocionVenta"))

#MOSTRAR
@app.route('/Promociones_Venta/consultar/<int:pagina>')
@login_required
def consultarPromocionesVenta(pagina):
    if current_user.is_admin():
        p = Promociones_Venta()
        if request.args.get('filtro'):
            return render_template('Promociones_Venta/ConsultarFiltro.html', promocion_venta_sin_paginacion = p.filtrar(request.args.get('filtro')), pagina = pagina)
        else:
                return render_template('Promociones_Venta/ConsultarPromocion.html', promociones_venta = p.paginar(pagina), pagina = pagina)
    else:
        abort(404)

#Eliminar
@app.route("/PromocionesVenta/eliminar/<int:id>")
def eliminarPromocionVenta(id):
    p = Promociones_Venta()
    p.eliminar(id)
    flash('¡Se ha eliminado el promocion venta!')
    return redirect(url_for('consultarPromocionesVenta', pagina=1))

@app.route("/Facturas/json/<int:id>")
def consultarFacturasJSON(id):
    ventas = Ventas()
    if id==0:
        lista=ventas.ventasCliente(id)
    else:
        lista=ventas.ventasCliente(id)
    #print(lista)
    listaFacturas=[]
    cliente = Cliente()
    cliente = cliente.consultaIndividual(id)
    #Generacion de un diccionario para convertir los datos a JSON
    for fac in lista:
        fac_dic={'Folio':fac.idVenta}
        listaFacturas.append(fac_dic)
    #print(listaProductos)
    var_json=json.dumps(listaFacturas)
    return var_json

@app.route("/Tarjetas/json/<int:id>")
def consultarTarjetasJSON(id):
    tarjetas = Tarjetas()
    nomina = Nomina()
    nomina = nomina.nominaCliente(id)
    if id==0:
        lista=tarjetas.consultaTarjetaUsuario(id)
    else:
        lista=tarjetas.consultaTarjetaUsuario(id)
    #print(lista)
    listaTarjetas=[]
    #Generacion de un diccionario para convertir los datos a JSON
    for tar in lista:
        tar_dic={'Tarjeta':tar.numero_tarjeta,'idTarjeta':tar.idTarjeta,'idNomina':nomina.idnomina}
        listaTarjetas.append(tar_dic)
    #print(listaProductos)
    var_json=json.dumps(listaTarjetas)
    return var_json

#FIN_CRUD_PROMOCIONES_VENTA
if __name__=='__main__':
    db.init_app(app)#Inicializar la BD - pasar la configuración de la url de la BD
    app.run(debug=True)

