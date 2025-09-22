#---------------------------------
# Autor: Fédor Tikhomirov
#---------------------------------

import os
import sqlite3
from datetime import datetime
from typing import Optional

# Imports de Fast API
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Ruta a Base de Datos
DB_PATH = os.path.join(os.path.dirname(__file__), "datosSensores.db")

# Referencia a carpetas de HTML y JS
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Modelo de datos
class SensorData(BaseModel):
    Fecha: Optional[str] = None ## Fecha opcional porque si no se recibe la crea la función
    Contador: int
    CO2: float

#SECTION - Endpoints

# Endpoint de POST, recibe el modelo de datos previamente declarado
@app.post("/datosSensor")
async def recibir_datos(data: SensorData):
    # Genera una fecha si el campo está vacio
    fechahora = data.Fecha or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try: # Conexión con la BBDD
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO datosSensor (Fecha, Contador, CO2) VALUES (?, ?, ?)",
            (fechahora, data.Contador, data.CO2)
        ) # Inserta o sustituye (si ya existe cierto contador) los datos en la BBDD
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close() # Pase lo que pase cierra la conexión

    return {"status": "ok"} # Si todo fue bien, devuelve 200 OK

# Endpoint de GET, devuelve un JSON de los datos con la última fecha
@app.get("/ultimo")
async def ultimo():
    try: ## Conexión con la BBDD
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT Fecha, Contador, CO2 FROM datosSensor ORDER BY Fecha DESC LIMIT 1")
        row = cursor.fetchone()
    finally:
        conn.close()

    if row:
        return {"Fecha": row[0], "Contador": row[1], "CO2": row[2]}
    else:
        raise HTTPException(status_code=404, detail="No data")

# Devuelve el index.html renderizado al acceder al directorio raíz (cosas de FastAPI)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})