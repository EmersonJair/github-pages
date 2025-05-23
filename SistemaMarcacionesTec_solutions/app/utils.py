from functools import wraps
from flask import session, redirect, url_for

from app.models import Usuario

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