import os
import sqlite3
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "datosSensores.db")

@app.route('/datosSensor', methods=['POST'])
def recibir_datos():
    data = request.get_json()
    if not data or 'Contador' not in data or 'CO2' not in data:
        return jsonify({"error": "Datos inválidos"}), 400
    
    fechahora = data.get('Fecha', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    contador = data['Contador']
    co2 = data['CO2']

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO datosSensor (Fecha, Contador, CO2) VALUES (?, ?, ?)",
        (fechahora, contador, co2)
    )
    conn.commit()
    conn.close()

    return jsonify({"status": "ok"}), 200
