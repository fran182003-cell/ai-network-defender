from pydantic import BaseModel, Field

class NetworkLog(BaseModel):
    ip_origen: str = Field(..., description="Dirección IP de origen", example="192.168.1.15")
    tamano_paquete: float = Field(..., gt=0)
    latencia: float = Field(..., ge=0)
    intentos_conexion: float = Field(..., ge=1)

class ResponseModel(BaseModel):
    status: str
    mensaje: str
    accion: str = None

class Token(BaseModel):
    access_token: str
    token_type: str