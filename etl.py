import pandas as pd
import sqlite3
import random
from datetime import datetime

def generar_datos(n=5):
    conn = sqlite3.connect("consumo.db")
    cursor = conn.cursor()

    ubicaciones = ["Oficina", "Sala de Servidores", "Aula 1", "Aula 2", "Pasillo", "Recepción"]
    
    for _ in range(n):
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora = datetime.now().strftime("%H:%M:%S")
        ubicacion = random.choice(ubicaciones)
        consumo = round(random.uniform(0.5, 5.0), 2)
        cursor.execute(
            "INSERT INTO consumo_electrico(fecha, hora, ubicacion, consumo_kw) VALUES (?, ?, ?, ?)",
            (fecha, hora, ubicacion, consumo)
        )
    
    conn.commit()
    conn.close()

def ejecutar_etl():
    conn = sqlite3.connect("consumo.db")
    df = pd.read_sql_query("SELECT * FROM consumo_electrico", conn)
    df['fecha_hora'] = pd.to_datetime(df['fecha'] + ' ' + df['hora'])
    df['hora'] = df['fecha_hora'].dt.hour
    resumen = df.groupby(['fecha', 'hora', 'ubicacion'])['consumo_kw'].sum().reset_index()
    resumen.to_csv("resumen_consumo.csv", index=False)
    conn.close()

