import os
import sqlite3
from flask import Flask, request, jsonify
from datetime import datetime
from flask import render_template

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

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO datosSensor (Fecha, Contador, CO2) VALUES (?, ?, ?)",
            (fechahora, contador, co2)
        )
        conn.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

    return jsonify({"status": "ok"}), 200

@app.route('/ultimo', methods=['GET'])
def ultimo():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT Fecha, Contador, CO2 FROM datosSensor ORDER BY Fecha DESC LIMIT 1")
        row = cursor.fetchone()
    finally:
        conn.close()

    if row:
        return jsonify({
            "Fecha": row[0],
            "Contador": row[1],
            "CO2": row[2]
        })
    else:
        return jsonify({"error": "No data"}), 404
    

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

