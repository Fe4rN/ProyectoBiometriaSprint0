# tests/test_app.py
import sys
import os
import sqlite3
import tempfile
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import app
import logicaNegocio

client = TestClient(app.app)

@pytest.fixture(scope="function", autouse=True)
def test_db():

    tmpfile = tempfile.NamedTemporaryFile(delete=False)
    db_path = tmpfile.name
    tmpfile.close()

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

    app.DB_PATH = db_path
    logicaNegocio.DB_PATH = db_path

    yield db_path

    os.remove(db_path)


def test_insert_and_get_last():
    data = {
        "Fecha": "2025-09-24 12:00:00",
        "Contador": 42,
        "CO2": 415
    }
    response = client.post("/datosSensor", json=data)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    response = client.get("/ultimo")
    assert response.status_code == 200
    result = response.json()

    assert result["Fecha"] == "2025-09-24 12:00:00"
    assert result["Contador"] == 42
    assert result["CO2"] == 415

def test_get_last_without_data():
    # No data inserted → should return 404
    response = client.get("/ultimo")
    assert response.status_code == 404
    assert response.json()["detail"] == "No data"