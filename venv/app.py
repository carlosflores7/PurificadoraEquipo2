from datetime import timedelta

from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_bootstrap import Bootstrap
from modelo.Dao import db,Categoria,Producto,Usuario ,Tarjeta
from flask_login import login_required,login_user,logout_user,current_user,LoginManager
app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user_shopitesz1:Banano0420@localhost/shopitesz'#usuario del bruno
#app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://User_Shopitesz:popo@localhost/shopitesz'#USuario Adame
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
    app.permanent_session_lifetime=timedelta(minutes=10)

@app.route("/")
def inicio():
    #return "Bienvenido a la tienda en linea Shopitesz"
    return render_template('principal.html')

@app.route('/Usuarios/iniciarSesion')
def mostrar_login():
    if current_user.is_authenticated:
        return render_template('principal.html')
    else:
        return render_template('usuarios/login.html')

@login_manager.user_loader
def cargar_usuario(id):
    return Usuario.query.get(int(id))

@app.route('/Usuarios/nuevo')
def nuevoUsuario():
    if current_user.is_authenticated and not current_user.is_admin:
        return render_template('principal.html')
    else:
        return render_template('usuarios/registrarCuenta.html')

@app.route('/Usuarios/agregar',methods=['post'])
def agregarUsuario():
    try:
        usuario=Usuario()
        usuario.nombreCompleto=request.form['nombre']
        usuario.telefono=request.form['telefono']
        usuario.direccion=request.form['direccion']
        usuario.email=request.form['email']
        usuario.genero=request.form['genero']
        usuario.password=request.form['password']
        usuario.tipo=request.values.get("tipo","Comprador")
        usuario.estatus='Activo'
        usuario.agregar()
        flash('¡ Usuario registrado con exito')
    except:
        flash('¡ Error al agregar al usuario !')
    return render_template('usuarios/registrarCuenta.html')


@app.route("/Usuarios/validarSesion",methods=['POST'])
def login():
    correo=request.form['correo']
    password=request.form['password']
    usuario=Usuario()
    user=usuario.validar(correo,password)
    if user!=None:
        login_user(user)

        return render_template('principal.html')
    else:
        flash('Nombre de usuario o contraseña incorrectos')
        return render_template('usuarios/login.html')

@app.route('/Usuarios/cerrarSesion')
@login_required
def cerrarSesion():
    logout_user()
    return redirect(url_for('mostrar_login'))

@app.route('/Usuarios/verPerfil')
@login_required
def verperfil():
    #return render_template('usuarios/editar.html')
    return render_template('usuarios/VerPerfil.html')

@app.route('/Usuarios/editarPerfil')
@login_required
def ediatarPerfil():
    return render_template('usuarios/editar.html')
#CRU Tarjetas
@app.route('/Usuarios/verTarjetas/<int:id>')
@login_required
def verTarjetas(id):
    tar=Tarjeta()
    return render_template("/tarjetas/tarjetaregistrada.html",Tarjetas=tar.consultaGeneral(id))

@app.route('/usuarios/agregarNuevaTarjeta/<int:id>')
@login_required
def agregarTarjeta(id):
    if current_user.is_authenticated :
        return render_template("/tarjetas/tarjetas.html")

@app.route("/tarjetas/agregar/<int:id>",methods=['post'])
@login_required
def subirtarjeta(id):
    try:
        if current_user.is_authenticated:
                try:
                    tar=Tarjeta()
                    tar.idUsuario=request.form['ID']
                    tar.noTarjeta=request.form['noTarjeta']
                    tar.saldo=request.form['Saldo']
                    tar.banco=request.form['Banco']
                    tar.estatus =request.form['Estatus']
                    tar.agregar()
                    flash('!tarjeta agregada con exito¡')
                except:
                    flash('! Error al agregar tarjeta¡')
                return render_template("/tarjetas/tarjetaregistrada.html",Tarjetas=tar.consultaGeneral(id))
        else:
            return redirect(url_for('mostrar_login'))
    except:
        #abort(500)
        return render_template("/")

@app.route('/Tarjeta/<int:id>')
@login_required
def EditarTarjetas(id):
    if current_user.is_authenticated():
        tar=Tarjeta()
        return render_template('tarjetas/editar.html', tar=tar.consulta(id))
    else:
        return redirect(url_for('mostrar_login'))
@app.route('/tarjeta/editar/<int:id>',methods=['POST'])
@login_required
def editandoTarjeta(id):
    if current_user.is_authenticated:
        try:
            tar=Tarjeta()
            tar.idTarjeta=request.form['ID']
            tar.idUsuario=request.form['IDU']
            tar.noTarjeta=request.form['noTarjeta']
            tar.saldo=request.form['Saldo']
            tar.banco=request.form['Banco']
            tar.estatus=request.form['Estatus']
            tar.editar()
            flash('! Tarjeta editada con exito')
        except:
            flash('! Error al editar el producto')
        return render_template("/tarjetas/tarjetaregistrada.html",Tarjetas=tar.consultaGeneral(id))
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/tarjeta/eliminar/<int:id>')
@login_required
def eliminarTarjeta(id):
    if  current_user.is_authenticated():
        try:
            tar=Tarjeta()
            tar.eliminar(id)
            flash('Tarjeta Eliminada')
        except:
            flash('Error al eliminar tarjeta')
        return redirect((url_for('verperfil')))
    else:
        return redirect(url_for('mostrar_login'))

#Fin CRUD Tarjetas

#fin de manejo de usuarios


#incio de CRUD DE PRODUCTOS
@app.route("/productos")
def consultarProductos():
    #return "Retorna la lista de productos"
    producto=Producto()
    return render_template("productos/consultaGeneral.html",productos=producto.consultaGeneral())

@app.route('/productos/consultarImagen/<int:id>')
def consultarImagenProducto(id):
    prod=Producto()
    return prod.consultarImagen(id)

@app.route('/productos/consultarEspecificaciones/<int:id>')
def consultarEspecificionesProducto(id):
    prod=Producto()
    return prod.consultarEspecificaciones(id)

@app.route('/productos/nuevo')
@login_required
def nuevoProducto():
    if current_user.is_authenticated and current_user.is_vendedor():
            return render_template('productos/agregar.html')
    else:
        #abort(404)
        return
@app.route("/productos/agregar",methods=['post'])
@login_required
def agregarProducto():
    try:
        if current_user.is_authenticated:
            if current_user.is_vendedor():
                try:
                    prod=Producto()
                    prod.idCategoria=request.form['idcategoria']
                    prod.nombre=request.form['nombre']
                    prod.descripcion=request.form['descripcion']
                    prod.precioVenta=request.form['precioventa']
                    prod.existencia=request.form['existencia']
                    prod.foto=request.files['foto'].stream.read()
                    prod.especificaciones=request.files['especificaciones'].stream.read()
                    prod.estatus ='Activo'
                    prod.agregar()
                    flash('!Prodcuto agregado con exito¡')
                except:
                    flash('! Error al agregar producto¡')
                return redirect(url_for('consultarProductos'))
            else:
                #abort(404)
                return
        else:
            return redirect(url_for('mostrar_login'))
    except:
        #abort(500)
        return

@app.route('/productos/<int:id>')
@login_required
def consultaProductos(id):
    if current_user.is_authenticated and current_user.is_vendedor():
        prod=Producto()
        return render_template('productos/editar.html',prod=prod.consultaIndividuall(id))
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/productos/editar',methods=['POST'])
@login_required
def editarProducto():
    if current_user.is_authenticated and current_user.is_vendedor():
        try:
            prod=Producto()
            prod.idProducto = request.form['id']
            prod.idCategoria=request.form['idCategoria']
            prod.nombre=request.form['nombre']
            prod.descripcion = request.form['descripcion']
            prod.precioVenta = request.form['precioVenta']
            prod.existencia = request.form['existencia']
            especificaciones=request.files['especificaciones'].stream.read()
            foto=request.files['foto'].stream.read()
            if foto and especificaciones:
                prod.especificaciones=especificaciones
                prod.foto=foto
                prod.estatus=request.values.get("estatus")
                prod.editar()
                flash('! Producto editada con exito')
        except:
            flash('! Error al editar el producto')

        return redirect(url_for('consultarProductos'))
    else:
        return redirect(url_for('mostrar_login'))


@app.route('/productos/eliminar/<int:id>')
@login_required
def eliminarProductos(id):
    if current_user.is_authenticated and current_user.is_vendedor():
        try:
            prod=Producto()
            prod.eliminacionLogica(id)
            flash('Producto eliminado con exito')
        except:
            flash('Error al eliminar el producto')

        return redirect(url_for('consultarProductos'))
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/productis/eliminacionfisica/<int:id>')
@login_required
def eliminacionfisicaproducto(id):
    if  current_user.is_authenticated and current_user.is_vendedor():
        try:
            prod=Producto()
            prod.eliminar(id)
            flash('Producto eliminado')
        except:
            flash('Error al eliminar Producto')
        return redirect((url_for('consultarProductos')))
    else:
        return redirect(url_for('mostrar_login'))



#Fin Cru de productos

@app.route("/cesta")
def consultarCesta():
    return "consultando la cesta de compra"

@app.route("/productos/categoria/<int:id>")
def consultarProductosCategoria(id):
    return "consultando los productos de la cetogoria: "+str(id)

@app.route("/clientes/<string:nombre>")
def consultarCliente(nombre):
    return "consultando al cliente:"+nombre



#CRUD de Categorias
@app.route('/Categorias')
def consultaCategorias():
    cat=Categoria()
    return render_template('categorias/consultaGeneral.html',categorias=cat.consultaGeneral())

@app.route('/Categorias/consultarImagen/<int:id>')
def consultarImagenCategoria(id):
    cat=Categoria()
    return cat.consultarImagen(id)


@app.route('/Categorias/nueva')
@login_required
def nuevaCategoria():
    if current_user.is_authenticated and current_user.is_admin():
        return render_template('categorias/agregar.html')
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/Categorias/agregar',methods=['post'])
@login_required
def agregarCategoria():
    try:
        if current_user.is_authenticated:
            if current_user.is_admin():
                try:
                    cat = Categoria()
                    cat.nombre = request.form['nombre']
                    cat.imagen = request.files['imagen'].stream.read()
                    cat.estatus = 'Activa'
                    cat.agregar()
                    flash('¡ Categoria agregada con exito !')
                except:
                    flash('¡ Error al agregar la categoria !')
                return redirect(url_for('consultaCategorias'))
            else:
               # abort(404)
                return

        else:
            return redirect(url_for('mostrar_login'))
    except:
        #abort(500)
        return

@app.route('/Categorias/<int:id>')
@login_required
def consultarCategoria(id):
    if current_user.is_authenticated and current_user.is_admin():
        cat=Categoria()
        return render_template('categorias/editar.html',cat=cat.consultaIndividuall(id))
    else:
        return redirect(url_for('mostrar_login'))


@app.route('/Categorias/editar',methods=['POST'])
@login_required
def editarCategoria():
    if current_user.is_authenticated and current_user.is_admin():
        try:
            cat=Categoria()
            cat.idCategoria=request.form['id']
            cat.nombre=request.form['nombre']
            imagen=request.files['imagen'].stream.read()
            if imagen:
                cat.imagen=imagen
            cat.estatus=request.values.get("estatus","Inactiva")
            cat.editar()
            flash('¡ Categoria editada con exito !')
        except:
            flash('¡ Error al editar la categoria !')

        return redirect(url_for('consultaCategorias'))
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/Categorias/eliminar/<int:id>')
@login_required
def eliminarCategoria(id):
    if current_user.is_authenticated and current_user.is_admin():
        try:
            categoria=Categoria()
            #categoria.eliminar(id)
            categoria.eliminacionLogica(id)
            flash('Categoria eliminada con exito')
        except:
            flash('Error al eliminar la categoria')
        return redirect(url_for('consultaCategorias'))
    else:
        return redirect(url_for('mostrar_login'))

#Fin del crud de categorias


@app.route("/pedidosclt")
def consultarPedidos():
    #return "Retorna la lista de productos"
    return render_template("pedidosclt/pedidocl.html")

@app.route("/pedidosclt/pedidosdetalle")
def detallesPeddidos():
    return render_template("pedidosclt/pedidocliente.html")

@app.route("/pedidosclt/pedidospedir")
def pedidospedir():
    return render_template("pedidosclt/pedidopedircl.html")

@app.route("/pedidosclt/pedidosclvarios")
def pedidosclvarios():
    return render_template("pedidosclt/pedidosclvarios.html")

@app.route("/pedidosclt/pedidoscluno")
def pedidoscluno():
    return render_template("pedidosclt/pedidoscluno.html")


if __name__=='__main__':
    db.init_app(app)#Inicializar la BD - pasar la configuración de la url de la BD
    app.run(debug=True)