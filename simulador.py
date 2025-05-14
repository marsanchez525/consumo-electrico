import sqlite3
import random
import time
from datetime import datetime

# Conectar o crear la base de datos SQLite
conn = sqlite3.connect("consumo.db")
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS consumo_electrico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha TEXT,
    hora TEXT,
    ubicacion TEXT,
    consumo_kw REAL
)
""")
conn.commit()

# Ubicaciones simuladas
ubicaciones = ["Oficina", "Sala de Servidores", "Aula 1", "Aula 2", "Pasillo", "Recepción"]

def generar_dato():
    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")
    ubicacion = random.choice(ubicaciones)
    consumo = round(random.uniform(0.5, 5.0), 2)  # Simula entre 0.5 y 5 KW

    cursor.execute("INSERT INTO consumo_electrico (fecha, hora, ubicacion, consumo_kw) VALUES (?, ?, ?, ?)",
                   (fecha, hora, ubicacion, consumo))
    conn.commit()
    print(f"[✓] Dato guardado: {fecha} {hora} - {ubicacion}: {consumo} KW")

# Simular cada 10 segundos (puedes cambiar a 60 para simular minutos)
while True:
    generar_dato()
    time.sleep(10)
