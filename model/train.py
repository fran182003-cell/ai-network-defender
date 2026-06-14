import numpy as np
import pickle
import os
from sklearn.ensemble import IsolationForest

def train_model():
    print("Generando datos sintéticos de red...")
    np.random.seed(42)
    
    # Generar datos normales y anómalos
    X_normal = np.random.normal(loc=[500, 20, 1], scale=[50, 5, 0.1], size=(1000, 3))
    X_ataque = np.random.normal(loc=[5000, 200, 50], scale=[1000, 50, 10], size=(50, 3))
    X_train = np.vstack([X_normal, X_ataque])

    print("Entrenando Isolation Forest...")
    modelo = IsolationForest(contamination=0.05, random_state=42)
    modelo.fit(X_train)

    os.makedirs('model', exist_ok=True)
    with open('model/model.pkl', 'wb') as f:
        pickle.dump(modelo, f)
    
    # Guardar un dataset de prueba para evaluate.py
    X_test_normal = np.random.normal(loc=[500, 20, 1], scale=[50, 5, 0.1], size=(200, 3))
    X_test_ataque = np.random.normal(loc=[5000, 200, 50], scale=[1000, 50, 10], size=(10, 3))
    
    with open('model/test_data.pkl', 'wb') as f:
        pickle.dump((X_test_normal, X_test_ataque), f)

if __name__ == "__main__":
    train_model()