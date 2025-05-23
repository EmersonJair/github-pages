from flask import Blueprint, render_template, request, redirect, url_for, session
from app import db
from app.models import Usuario, Empleado, Marcacion
from datetime import datetime
from functools import wraps

bp = Blueprint('main', __name__)

# Decorador para proteger rutas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('usuario_id') is None:
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        usuario_id = session.get('usuario_id')
        usuario = Usuario.query.get(usuario_id)
        if not usuario or usuario.rol != 'admin':
            return "Acceso denegado", 403  # O redirigir a una página de error
        return f(*args, **kwargs)
    return decorated_function

# Rutas
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usuario = Usuario.query.filter_by(username=username).first()

        if usuario and usuario.check_password(password):
            session['usuario_id'] = usuario.id
            return redirect(url_for('main.dashboard'))
        else:
            return render_template('login.html', error='Credenciales inválidas')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    session.pop('usuario_id', None)
    return redirect(url_for('main.index'))

@bp.route('/dashboard')
@login_required
def dashboard():
    usuario_id = session.get('usuario_id')
    empleado = Empleado.query.filter_by(usuario_id=usuario_id).first()
    return render_template('dashboard.html', empleado=empleado)

@bp.route('/marcar', methods=['POST'])
@login_required
def marcar():
    data = request.form
    marcacion_tipo = data['marcacion']
    hora = datetime.now().time()
    usuario_id = session.get('usuario_id')
    empleado = Empleado.query.filter_by(usuario_id=usuario_id).first()

    marcacion_del_dia = Marcacion.query.filter_by(empleado_id=empleado.id, fecha=datetime.utcnow().date()).first()
    if not marcacion_del_dia:
        marcacion_del_dia = Marcacion(empleado_id=empleado.id)
        db.session.add(marcacion_del_dia)

    if marcacion_tipo == 'inicio_jornada':
        marcacion_del_dia.inicio_jornada = hora
    elif marcacion_tipo == 'salida_almuerzo':
        marcacion_del_dia.salida_almuerzo = hora
    elif marcacion_tipo == 'entrada_almuerzo':
        marcacion_del_dia.entrada_almuerzo = hora
    elif marcacion_tipo == 'fin_jornada':
        marcacion_del_dia.fin_jornada = hora

    db.session.commit()
    return redirect(url_for('main.dashboard'))

@bp.route('/consultar_marcaciones', methods=['GET', 'POST'])
@login_required
def consultar_marcaciones():
    usuario_id = session.get('usuario_id')
    empleado = Empleado.query.filter_by(usuario_id=usuario_id).first()
    marcaciones = []
    desde = None
    hasta = None

    if request.method == 'POST':
        desde_str = request.form.get('desde')
        hasta_str = request.form.get('hasta')

        if desde_str and hasta_str:
            try:
                desde = datetime.strptime(desde_str, '%Y-%m-%d').date()
                hasta = datetime.strptime(hasta_str, '%Y-%m-%d').date()
                marcaciones = Marcacion.query.filter(
                    Marcacion.empleado_id == empleado.id,
                    Marcacion.fecha >= desde,
                    Marcacion.fecha <= hasta
                ).all()
            except ValueError:
                # Manejar el error si las fechas no tienen el formato correcto
                pass

    return render_template('consultar_marcaciones.html', marcaciones=marcaciones, empleado=empleado, desde=desde, hasta=hasta)

@bp.route('/')
def index():
    return render_template('login.html')

# Rutas de administración (ejemplo)
@bp.route('/admin')
@login_required
@admin_required
def admin_panel():
    return "Panel de administración"