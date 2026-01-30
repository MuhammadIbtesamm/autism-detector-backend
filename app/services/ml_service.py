import joblib
import numpy as np
import os

# Path to backend folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ML_DIR = os.path.join(BASE_DIR, "ml")

model = joblib.load(os.path.join(ML_DIR, "model.pkl"))
scaler = joblib.load(os.path.join(ML_DIR, "scaler.pkl"))

def predict_autism_risk(answers: list[int], age: int):
    if len(answers) != 10:
        raise ValueError("Exactly 10 answers required")

    # Scale age (same as training)
    age_scaled = scaler.transform([[age]])[0][0]

    # Combine answers + age
    features = answers + [age_scaled]
    X = np.array(features).reshape(1, -1)

    probability = model.predict_proba(X)[0][1]
    return probability
