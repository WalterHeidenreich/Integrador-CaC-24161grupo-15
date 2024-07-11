import sqlite3

# Conexión a la base de datos
conn = sqlite3.connect('consultas.db')
c = conn.cursor()

# Añadir columnas "nota" y "fecha" a la tabla "consultas"
c.execute("ALTER TABLE consultas ADD COLUMN nota TEXT")
c.execute("ALTER TABLE consultas ADD COLUMN fecha TEXT")

conn.commit()
conn.close()
