from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import sqlite3
import base64
from markupsafe import Markup
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tu_secreto_aqui'  # Necesario para usar flash

# Conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect('consultas.db')
    conn.row_factory = sqlite3.Row
    return conn

# Filtro para codificar en base64
@app.template_filter('b64encode')
def b64encode_filter(data):
    return Markup(base64.b64encode(data).decode('utf-8'))

# Ruta para mostrar el formulario HTML
@app.route('/')
def index():
    return render_template('contacto.html')

# Ruta para recibir datos del formulario (POST)
@app.route('/submit', methods=['POST'])
def submit():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    pregunta = request.form['pregunta']
    imagen = request.files['imagen'].read() if 'imagen' in request.files else None
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO consultas (nombre, apellido, email, pregunta, imagen, fecha) VALUES (?, ?, ?, ?, ?, ?)",
              (nombre, apellido, email, pregunta, imagen, fecha))
    conn.commit()
    conn.close()

    flash('Su consulta fue enviada exitosamente.')
    return redirect(url_for('index'))

# Ruta para obtener todos los registros y mostrar en HTML (GET)
@app.route('/consultas', methods=['GET'])
def get_consultas():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM consultas")
    consultas = c.fetchall()
    conn.close()
    return render_template('consultas.html', consultas=consultas)

# Ruta para actualizar un registro (POST)
@app.route('/consultas/editar/<int:id>', methods=['POST'])
def update_consulta(id):
    conn = get_db_connection()
    c = conn.cursor()
    consulta = c.execute("SELECT * FROM consultas WHERE id = ?", (id,)).fetchone()
    if consulta is None:
        return "Consulta no encontrada", 404

    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    pregunta = request.form['pregunta']
    nueva_imagen = request.files['imagen'].read() if 'imagen' in request.files else None
    nota = request.form['nota']

    # Mantener la imagen existente si no se sube una nueva
    imagen = consulta['imagen'] if not nueva_imagen else nueva_imagen

    c.execute("UPDATE consultas SET nombre = ?, apellido = ?, email = ?, pregunta = ?, imagen = ?, nota = ? WHERE id = ?",
              (nombre, apellido, email, pregunta, imagen, nota, id))
    conn.commit()
    conn.close()

    flash('Consulta actualizada exitosamente.')
    return redirect(url_for('get_consultas'))

# Ruta para eliminar un registro (POST)
@app.route('/consultas/eliminar/<int:id>', methods=['POST'])
def delete_consulta(id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM consultas WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    flash('Consulta eliminada exitosamente.')
    return redirect(url_for('get_consultas'))

if __name__ == '__main__':
    app.run(debug=True)
