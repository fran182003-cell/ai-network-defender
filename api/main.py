from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from api.schemas import NetworkLog, ResponseModel, Token
from api.logger import get_logger
import pickle
import numpy as np

logger = get_logger("ai_gateway")
app = FastAPI(title="Zero Trust AI Gateway", version="2.0.0")

# --- SEGURIDAD JWT (Simulación) ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
FAKE_USER = {"username": "admin", "password": "password123"}

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != FAKE_USER["username"] or form_data.password != FAKE_USER["password"]:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")
    return {"access_token": form_data.username, "token_type": "bearer"}

# --- LÓGICA DE IA ---
try:
    with open('model/model.pkl', 'rb') as f:
        modelo = pickle.load(f)
except FileNotFoundError:
    logger.error("Artefacto model.pkl no encontrado.")
    modelo = None

blacklist_ips = set()

# El endpoint ahora exige un token válido (Depends(oauth2_scheme))
@app.post("/ingest", response_model=ResponseModel)
async def ingest_traffic(log: NetworkLog, token: str = Depends(oauth2_scheme)):
    if modelo is None:
        raise HTTPException(status_code=500, detail="Modelo no disponible.")

    if log.ip_origen in blacklist_ips:
        logger.warning(f"Acceso denegado (Zero Trust). IP: {log.ip_origen}")
        raise HTTPException(status_code=403, detail="Tráfico bloqueado: IP en Blacklist")
    
    caracteristicas = np.array([[log.tamano_paquete, log.latencia, log.intentos_conexion]])
    prediccion = modelo.predict(caracteristicas)[0]
    
    if prediccion == -1:
        blacklist_ips.add(log.ip_origen)
        logger.error(f"Anomalía detectada. Bloqueando IP: {log.ip_origen}")
        return ResponseModel(status="alerta", mensaje="Anomalía detectada.", accion="bloqueo")
    
    return ResponseModel(status="ok", mensaje="Tráfico legítimo.")