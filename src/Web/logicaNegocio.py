#---------------------------------
# Autor: Fédor Tikhomirov
# Fecha: 10 de octubre de 2025
#---------------------------------


import os
import sqlite3
from datetime import datetime
from typing import Optional
from fastapi import HTTPException

# Ruta a la Base de Datos
DB_PATH = os.path.join(os.path.dirname(__file__), "datosSensores.db")

#------------------------------------------------------------------
# Esta función inserta los datos a la base de datos
# String:fecha, N:contador, R:co2 --> insertar_datos()
#                     Código HTTP <--
#------------------------------------------------------------------

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

#------------------------------------------------------------------
# Esta función recibe los ultimos datos guardado en la base de datos
# String:fecha, N:contador, R:co2 | HTTP: 404 <-- obtener_ultimo()
#------------------------------------------------------------------

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
