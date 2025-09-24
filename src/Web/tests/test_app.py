import os
import sqlite3
import tempfile
import pytest
from fastapi.testclient import TestClient
from Web import app

@pytest.fixture(scope="function", autouse=True)
def test_db(monkeypatch):
    tmpfile = tempfile.NamedTemporaryFile(delete=False)
    db_path = tmpfile.name
    tmpfile.close()

    # Creamos una base de datos temporal
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE datosSensor (
            Fecha TEXT NOT NULL,
            Contador INTEGER NOT NULL,
            CO2 INTEGER NOT NULL,
            PRIMARY KEY(Contador)
        )
    """)
    conn.commit()
    conn.close()

    # Sustituimos el apth a la DDBB por la falsa
    monkeypatch.setattr(app, "DB_PATH", db_path)
    from Web import logicaNegocio
    monkeypatch.setattr(logicaNegocio, "DB_PATH", db_path)

    yield db_path  # Ejecutamos el test

    os.remove(db_path)  # Limpiamos

client = TestClient(app.app)

def test_insert_and_get_last():
    data = {
        "Fecha": "2025-09-24 12:00:00",
        "Contador": 42,
        "CO2": 415.7
    }
    response = client.post("/datosSensor", json=data)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    response = client.get("/ultimo")
    assert response.status_code == 200
    result = response.json()

    assert result["Fecha"] == "2025-09-24 12:00:00"
    assert result["Contador"] == 42
    assert abs(result["CO2"] - 415.7) < 1e-6


def test_get_last_without_data():
    response = client.get("/ultimo")
    assert response.status_code == 404
    assert response.json()["detail"] == "No data"
