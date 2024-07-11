import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('consultas.db')
c = conn.cursor()

# Crear la tabla consultas
c.execute('''
CREATE TABLE consultas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    email TEXT NOT NULL,
    pregunta TEXT NOT NULL,
    imagen BLOB
)
''')

# Guardar cambios y cerrar la conexión
conn.commit()
conn.close()

print("Base de datos y tabla creadas exitosamente")
