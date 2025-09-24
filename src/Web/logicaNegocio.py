import sqlite3
from datetime import datetime
from typing import Optional

from fastapi import HTTPException

# Ruta a la Base de Datos
import os
DB_PATH = os.path.join(os.path.dirname(__file__), "datosSensores.db")

def insertar_datos(fecha: Optional[str], contador: int, co2: float):
    # Inserta o actualiza datos en la base de datos.
    fechahora = fecha or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO datosSensor (Fecha, Contador, CO2) VALUES (?, ?, ?)",
            (fechahora, contador, co2)
        )
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

    return {"status": "ok"}


def obtener_ultimo():
    # Devuelve el último registro guardado en la base de datos.
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT Fecha, Contador, CO2 FROM datosSensor ORDER BY Fecha DESC LIMIT 1"
        )
        row = cursor.fetchone()
    finally:
        conn.close()

    if row:
        return {"Fecha": row[0], "Contador": row[1], "CO2": row[2]}
    else:
        raise HTTPException(status_code=404, detail="No data")
