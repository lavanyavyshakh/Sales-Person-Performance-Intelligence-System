import os
import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "ml_models")

# ================= LOAD MODELS =================
target_miss_model = joblib.load(
    os.path.join(MODEL_DIR, "target_miss_model.pkl")
)

consistency_model = joblib.load(
    os.path.join(MODEL_DIR, "consistency_model.pkl")
)

focus_model = joblib.load(
    os.path.join(MODEL_DIR, "focus_account_model.pkl")
)

# ================= TARGET MISS PREDICTION =================
def predict_target_miss(features):
    """
    features = [target_amount, achieved_amount, days_remaining]
    """
    columns = ["target_amount", "achieved_amount", "days_remaining"]

    df = pd.DataFrame([features], columns=columns)

    prob = target_miss_model.predict_proba(df)[0][1]

    return {
        "prediction": "At Risk" if prob > 0.6 else "Safe",
        "risk_percent": round(prob * 100, 2),
    }

# ================= PERFORMANCE CONSISTENCY =================
def predict_consistency(features):
    """
    features = [target_amount, achieved_amount]
    """
    columns = ["target_amount", "achieved_amount"]

    df = pd.DataFrame([features], columns=columns)

    result = consistency_model.predict(df)[0]
    return "Consistent" if result == 1 else "Inconsistent"


# ================= FOCUS ACCOUNT =================
def predict_focus_account(features):
    """
    features = [total_revenue, invoice_count, avg_invoice_value]
    """
    columns = ["total_revenue", "invoice_count", "avg_invoice_value"]


    df = pd.DataFrame([features], columns=columns)

    score = focus_model.predict(df)[0]

    if score > 70:
        return "High"
    elif score > 40:
        return "Medium"
    return "Low"
