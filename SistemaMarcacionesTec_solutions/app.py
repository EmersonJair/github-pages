from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tec_solutions.db'
db = SQLAlchemy(app)

class Empleado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dui = db.Column(db.String(10), unique=True)
    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    id_dui = data['id_dui']
    password = data['password']

    # Buscar usuario por ID o DUI
    empleado = Empleado.query.filter((Empleado.id == id_dui) | (Empleado.dui == id_dui)).first()

    if empleado and empleado.check_password(password):
        return jsonify({'success': True, 'message': 'Inicio de sesión exitoso'})
    else:
        return jsonify({'success': False, 'message': 'Credenciales inválidas'})

@app.route('/dashboard')
def dashboard():
    return "¡Bienvenido al dashboard!"

if __name__ == '__main__':
    app.run(debug=True)