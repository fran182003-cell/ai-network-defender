from fastapi.testclient import TestClient
from api.main import app, blacklist_ips

client = TestClient(app)

def get_token():
    response = client.post("/token", data={"username": "admin", "password": "password123"})
    return response.json()["access_token"]

def test_trafico_sin_token_rechazado():
    response = client.post("/ingest", json={"ip_origen": "1.1.1.1", "tamano_paquete": 100, "latencia": 10, "intentos_conexion": 1})
    assert response.status_code == 401 # Unauthorized

def test_trafico_normal_con_token():
    blacklist_ips.clear()
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/ingest", headers=headers, json={
        "ip_origen": "192.168.1.10",
        "tamano_paquete": 500,
        "latencia": 20,
        "intentos_conexion": 1
    })
    assert response.status_code == 200
    assert response.json()["status"] == "ok"