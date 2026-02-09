import joblib
from schema.user_input_schema import Transaction
import os
BASE_DIR =os.path.dirname(os.path.abspath(__file__))

# -----------------------------
# Load trained model
# -----------------------------
model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))   # <-- Load scaler

# -----------------------------
# VERSION Of MODEL
# -----------------------------
MODEL_VERSION='1.0.0'