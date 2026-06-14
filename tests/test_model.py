import pickle
import numpy as np

def test_modelo_detecta_anomalia_extrema():
    with open('model/model.pkl', 'rb') as f:
        modelo = pickle.load(f)
    
    # Simular un paquete absurdamente grande 
    ataque = np.array([[99999, 500, 100]])
    prediccion = modelo.predict(ataque)
    
    assert prediccion[0] == -1, "El modelo debería clasificar esto como anomalía (-1)"