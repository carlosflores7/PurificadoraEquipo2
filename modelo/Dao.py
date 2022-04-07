import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,BLOB,ForeignKey,Float,Date
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
db=SQLAlchemy()

class Usuario(UserMixin,db.Model):
    __tablename__='Usuarios'
    idUsuario=Column(Integer,primary_key=True)
    nombre=Column(String,nullable=False)
    correo=Column(String,unique=True)
    password_hash=Column(String(256),nullable=False)
    tipo=Column(String,nullable=False)
    estatus=Column(String,nullable=False)

    @property #Implementa el metodo Get (para acceder a un valor)
    def password(self):
        raise AttributeError('El password no tiene acceso de lectura')

    @password.setter #Definir el metodo set para el atributo password_hash
    def password(self,password):#Se informa el password en formato plano para hacer el cifrado
        self.password_hash=generate_password_hash(password)

    def validarPassword(self,password):
        return check_password_hash(self.password_hash,password)
    #Definición de los métodos para el perfilamiento
    def is_authenticated(self):
        return True

    def get_id(self):
        return self.idUsuario

    def is_active(self):
        if self.estatus=='1':
            return True
        else:
            return False

    def is_admin(self):
        if self.tipo=='Administrador':
            return True
        else:
            return False
    #Definir el método para la autenticacion
    def validar(self,correo,password):
        usuario=Usuario.query.filter(Usuario.correo==correo).first()
        if usuario!=None and usuario.validarPassword(password):
            return usuario
        else:
            return None
    #Método para agregar una cuenta de usuario
    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self,id):
        return self.query.get(id)

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminacionLogica(self,id):
        usuario = self.consultaIndividual(id)
        usuario.estatus = '0'
        usuario.editar()

    def paginar(self, pagina):
        return self.query.paginate(per_page=4, page=pagina, error_out=True)

    def consultaTipo(self, tipo):
        return self.query.filter(Usuario.tipo == tipo).all()

    def consultaNombre(self, nombre):
        return self.query.filter(Usuario.nombre == nombre).all()

class Vehiculo(db.Model):
    __tablename__ = 'Vehiculo'
    idVehiculo = Column(Integer, primary_key=True)
    placas = Column(String(10), nullable=False)
    tipo_de_vehiculo = Column(String(45), nullable=False)
    tipo_combustible = Column(String(45), nullable=False)
    capacidad_tanque = Column(String(45), nullable=False)
    modelo = Column(String(45), nullable=False)
    año = Column(String(4), nullable=False)
    capacidad_garrafones = Column(Integer, nullable=False)

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self,id):
        return self.query.get(id)

    def consultaGeneral(self):
        return self.query.all()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        obj = self.consultaIndividual(id)
        db.session.delete(obj)
        db.session.commit()

    def filtrar(self, filtro):
        return self.query.filter(Vehiculo.placas.like('%'+filtro+'%'))

    def paginar(self, pagina):
        return self.query.paginate(per_page=4, page=pagina, error_out=True)

    def consultarPlacas(self, placas):
        salida={"estatus":"","mensaje":""}
        vehiculo = None
        vehiculo = self.query.filter(Vehiculo.placas==placas).first()
        if vehiculo != None:
            salida['estatus']='Error'
            salida['mensaje'] = 'Las placas ' + placas + ' ya estan registradas'
        else:
            salida['estatus'] = 'Ok'
            salida['mensaje'] = 'Las placas ' + placas + ' estan libres'
        return salida


###Garrafones###

class Garrafones(db.Model):
    __tablename__ = 'garrafones'
    idGarrafon = Column(Integer, primary_key=True)
    Estado = Column(String(15), nullable=False)
    codigo = Column(String(10), nullable = False)
    capaciodad = Column(Integer, nullable=False)
    precio_retornable = Column(Float, nullable=False)
    precio_completo = Column(Float, nullable=False)

    def insertar(self):
          db.session.add(self)
          db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self,id):
        return self.query.get(id)

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        obj = self.consultaIndividual(id)
        db.session.delete(obj)
        db.session.commit()
    
    def filtro(self, filtro):
        return self.query.filter(Garrafones.codigo.like('%'+filtro+'%'))

    def paginacion(self,pagina):
        return self.query.paginate(per_page=2,page=pagina,error_out=True)

###Promociones###

class Promociones(db.Model):
    __tablename__='promociones'
    idpromocion=Column(Integer,primary_key=True)
    cantidad_max=Column(Integer,nullable=False)
    cantidad_min=Column(Integer,nullable=True)
    estatus=Column(Integer,nullable=False)
    porcentaje=Column(Float,nullable=False)

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self,id):
        return self.query.get(id)

    def consultaGeneral(self):
        return self.query.all()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        obj = self.consultaIndividual(id)
        db.session.delete(obj)
        db.session.commit()

    def eliminacionLogica(self, id):
        promocion = self.consultaIndividual(id)
        promocion.estatus=0
        promocion.actualizar()

    def paginacion(self,pagina):
        return self.query.paginate(per_page=3,page=pagina,error_out=True)





class Puesto(db.Model):
    __tablename__='puestos'
    idPuesto = Column(Integer,primary_key=True)
    nombre = Column(String(45),nullable=False)
    salario_max = Column(String(45),nullable=False)
    salario_min = Column(String(45),nullable=False)
    descripcion = Column(String(200),nullable=False)

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

class Empleado(db.Model):
    __tablename__='Empleado'
    idEmpleado = Column(Integer,primary_key=True)
    tipoEmpleado = Column(String(40),nullable=False)
    salario_por_dia = Column(String(45),nullable=False)
    turno = Column(String(45),nullable=False)
    nss = Column(String(45),nullable=False)
    Usuarios_idUsuario = Column(Integer, ForeignKey('Usuarios.idUsuario'))
    puestos_idPuesto = Column(Integer,ForeignKey('puestos.idPuesto'))
    usuario = relationship('Usuario',lazy='select')
    puesto = relationship('Puesto',lazy='select')

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def paginar(self,pagina):
        return self.query.paginate(per_page=4,page=pagina,error_out=True)

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminacionLogica(self,id):
        empleado = self.consultaIndividual(id)
        empleado.tipoEmpleado = 'I'
        empleado.editar()

class Tarjetas(db.Model):
    __tablename__='tarjetas'
    idTarjeta = Column(Integer, primary_key=True)
    Empleado_idEmpleado = Column(Integer,ForeignKey('Empleado.idEmpleado'))
    numero_tarjeta = Column(String(45),nullable=False)
    banco=Column(String(45),nullable=False)
    empleado = relationship('Empleado',lazy='select')

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self,id):
        return self.query.get(id)

    def consultaGeneral(self):
        return self.query.all()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        obj = self.consultaIndividual(id)
        db.session.delete(obj)
        db.session.commit()
