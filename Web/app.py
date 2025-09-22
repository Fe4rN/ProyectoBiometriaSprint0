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
from pydantic import BaseModel

app = FastAPI()

# Ruta a Base de Datos
DB_PATH = os.path.join(os.path.dirname(__file__), "datosSensores.db")

# Referencia a carpeta de HTMLs
templates = Jinja2Templates(directory="templates")

from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")

# Estructura de datos
class SensorData(BaseModel):
    Fecha: Optional[str] = None
    Contador: int
    CO2: float

# Endpoints
@app.post("/datosSensor")
async def recibir_datos(data: SensorData):
    fechahora = data.Fecha or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO datosSensor (Fecha, Contador, CO2) VALUES (?, ?, ?)",
            (fechahora, data.Contador, data.CO2)
        )
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

    return {"status": "ok"}


@app.get("/ultimo")
async def ultimo():
    try:
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


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})