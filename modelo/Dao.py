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