import joblib
from schema.user_input_schema import Transaction

# -----------------------------
# Load trained model
# -----------------------------
model = joblib.load("model/fraud_model_rf.pkl")
scaler = joblib.load("model/fraud_scaler.pkl")   # <-- Load scaler

# -----------------------------
# VERSION Of MODEL
# -----------------------------
MODEL_VERSION='1.0.0'