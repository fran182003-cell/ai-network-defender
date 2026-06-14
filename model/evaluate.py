import pickle
import numpy as np
from sklearn.metrics import classification_report

def evaluate_model():
    print("Evaluando métricas del modelo en pre-producción...")
    
    with open('model/model.pkl', 'rb') as f:
        modelo = pickle.load(f)
        
    with open('model/test_data.pkl', 'rb') as f:
        X_normal, X_ataque = pickle.load(f)

    # Predicciones (1 normal, -1 anomalía)
    pred_normal = modelo.predict(X_normal)
    pred_ataque = modelo.predict(X_ataque)

    # Etiquetas reales (1 normal, -1 anomalía)
    y_true = np.concatenate([np.ones(len(X_normal)), -np.ones(len(X_ataque))])
    y_pred = np.concatenate([pred_normal, pred_ataque])

    print("\nReporte de Clasificación (F1-Score, Recall):")
    print(classification_report(y_true, y_pred, target_names=["Anomalía", "Normal"]))

if __name__ == "__main__":
    evaluate_model()