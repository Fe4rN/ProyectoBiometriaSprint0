#---------------------------------
# Autor: Fédor Tikhomirov
# Fecha: 10 de octubre de 2025
#---------------------------------

import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

# Importa las funciones separadas
from logicaNegocio import insertar_datos, obtener_ultimo

app = FastAPI()

# Referencia a carpetas de HTML y JS
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Modelo de datos
class SensorData(BaseModel):
    Fecha: Optional[str] = None
    Contador: int
    CO2: float

# Endpoint de POST
@app.post("/datosSensor")
async def recibir_datos(data: SensorData):
    return insertar_datos(data.Fecha, data.Contador, data.CO2)

# Endpoint de GET
@app.get("/ultimo")
async def ultimo():
    return obtener_ultimo()

# Página principal
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})