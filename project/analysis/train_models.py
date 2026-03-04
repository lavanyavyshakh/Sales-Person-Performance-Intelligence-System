import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "datasets")
MODEL_DIR = os.path.join(BASE_DIR, "ml_models")

os.makedirs(MODEL_DIR, exist_ok=True)

# ================= TARGET MISS =================
df = pd.read_csv(os.path.join(DATASET_DIR, "target_miss.csv"))

X = df[
    ["target_amount", "achieved_amount",
     "invoice_count", "avg_invoice_value",
     "active_days"]
]
y = df["target_missed"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

target_miss_model = RandomForestClassifier(
    n_estimators=120, max_depth=6, random_state=42
)
target_miss_model.fit(X_train, y_train)

print("Target Miss Accuracy:",
      accuracy_score(y_test, target_miss_model.predict(X_test)))

joblib.dump(
    target_miss_model,
    os.path.join(MODEL_DIR, "target_miss_model.pkl")
)

# ================= CONSISTENCY =================
df = pd.read_csv(os.path.join(DATASET_DIR, "performance_consistency.csv"))

X = df[["target_amount", "achieved_amount"]]
y = (df["achieved_amount"] >= df["target_amount"]).astype(int)

consistency_model = RandomForestClassifier(
    n_estimators=100, max_depth=5, random_state=42
)
consistency_model.fit(X, y)

joblib.dump(
    consistency_model,
    os.path.join(MODEL_DIR, "consistency_model.pkl")
)

# ================= FOCUS ACCOUNT =================
df = pd.read_csv(os.path.join(DATASET_DIR, "focus_accounts.csv"))

X = df[["total_revenue", "invoice_count", "avg_invoice_value"]]
y = pd.cut(
    df["total_revenue"],
    bins=[0, 30000, 70000, 10**9],
    labels=[2, 1, 0]  # 0=High, 1=Medium, 2=Low
)

focus_model = RandomForestClassifier(n_estimators=100)
focus_model.fit(X, y)

joblib.dump(
    focus_model,
    os.path.join(MODEL_DIR, "focus_account_model.pkl")
)

print("✅ ALL .PKL MODELS CREATED")
