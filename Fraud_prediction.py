from pydantic import BaseModel , Field , computed_field , model_validator
import pickle

from fastapi import FastAPI, HTTPException 
import pandas as pd
import joblib


from schema.user_input_schema import Transaction 
from schema.output_response import RiskResponse
from model.predict import model , MODEL_VERSION , scaler



# -----------------------------
# Explicit feature schema
# -----------------------------
FEATURES = [
    "account_age_days",
    "total_transactions",
    "failed_payments",
    "transaction_amount",
    "transaction_hour",
    "is_vpn",
    "txn_count_last_1h",
    "location_mismatch",
    "avg_amount_last_30d"
]



# -----------------------------
# Initialize FastAPI
# -----------------------------
app = FastAPI(
    title="Fraud Detection API",
    description="Payment risk scoring service",
    version="1.0.0"
)

# ----------------------------- 
# Home  check
# -----------------------------
@app.get("/")
def home():
    return {"message":" Fraud Prediction API"}
# ----------------------------- 
# Health check
# -----------------------------
@app.get("/health")
def health():
    return {"status": "API is running",
            "version":MODEL_VERSION}

# -----------------------------
# Predict payment risk
# -----------------------------

@app.post("/predict")
def predict(txn: Transaction) -> RiskResponse:
    data = txn.model_dump()

    # Create dataframe in correct order
    df = pd.DataFrame([[data[f] for f in FEATURES]], columns=FEATURES)

    # SCALE FIRST
    df_scaled = scaler.transform(df)

    # Predict fraud probability
    fraud_prob = float(model.predict_proba(df_scaled)[0][1])
    risk_score = round(fraud_prob * 100, 2)

    # Risk bands
    if risk_score >= 80:
        risk_level = "HIGH"
        action = "BLOCK"
    elif risk_score >= 50:
        risk_level = "MEDIUM"
        action = "STEP_UP_AUTH"
    else:
        risk_level = "LOW"
        action = "ALLOW"

    # Confidence logic (simple but effective)
    confidence = round(max(fraud_prob, 1 - fraud_prob), 3)

    # Rule signals (example)
    triggered_rules = []
    if txn.is_vpn == 1:
        triggered_rules.append("VPN_USAGE")
    if txn.location_mismatch == 1:
        triggered_rules.append("LOCATION_MISMATCH")
    if txn.failed_payments >= 3:
        triggered_rules.append("MULTIPLE_FAILED_PAYMENTS")

    return RiskResponse(
        payment_risk_score=risk_score,
        risk_level=risk_level,
        recommended_action=action,
        confidence_score=confidence,
        model_version=MODEL_VERSION,
        triggered_rules=triggered_rules
    )
