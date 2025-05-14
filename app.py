from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.io as pio
from etl import ejecutar_etl, generar_datos

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        generar_datos(n=5)   # Simula 5 nuevos datos
        ejecutar_etl()       # Ejecuta ETL y genera el CSV

    # Cargar resumen
    try:
        df = pd.read_csv("resumen_consumo.csv")
        total_registros = len(df)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['fecha', 'hora', 'ubicacion', 'consumo_kw'])
        total_registros = 0

    # Crear gráfico
    if not df.empty:
        fig = px.bar(df, x='ubicacion', y='consumo_kw', color='fecha', title='Consumo por Ubicación y Fecha')
        grafico = pio.to_html(fig, full_html=False)
    else:
        grafico = "<p>No hay datos para mostrar.</p>"

    return render_template("index.html", 
        tabla=df.tail(20).to_html(classes="table table-striped"),
        grafico=grafico,
        total=total_registros
    )

if __name__ == '__main__':
    app.run(debug=True, port=3001)
