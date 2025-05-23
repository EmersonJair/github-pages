from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    rol = db.Column(db.String(50), default='empleado')  # 'admin' o 'empleado'
    empleado = db.relationship('Empleado', backref='usuario', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Usuario {self.username}>'

class Empleado(db.Model):
    __tablename__ = 'empleado'
    id = db.Column(db.Integer, primary_key=True)
    dui = db.Column(db.String(10), unique=True)
    nombre = db.Column(db.String(100))
    categoria = db.Column(db.String(50))
    institucion = db.Column(db.String(100))
    carnet = db.Column(db.String(20))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), unique=True, nullable=False)
    marcaciones = db.relationship('Marcacion', backref='empleado', lazy=True)

    def __repr__(self):
        return f'<Empleado {self.nombre}>'

class Marcacion(db.Model):
    __tablename__ = 'marcacion'
    id = db.Column(db.Integer, primary_key=True)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleado.id'), nullable=False)
    fecha = db.Column(db.Date, default=datetime.utcnow().date())
    inicio_jornada = db.Column(db.Time, nullable=True)
    salida_almuerzo = db.Column(db.Time, nullable=True)
    entrada_almuerzo = db.Column(db.Time, nullable=True)
    fin_jornada = db.Column(db.Time, nullable=True)

    def __repr__(self):
        return f'<Marcacion {self.fecha} - {self.empleado.nombre}>'