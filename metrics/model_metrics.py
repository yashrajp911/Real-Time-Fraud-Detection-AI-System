import pandas as pd
import joblib
import os
from sklearn.metrics import classification_report, confusion_matrix

# --- Load test data ---
test_df = pd.read_csv("D:/Project X/test_data/test_sample.csv")

# Separate features and labels
X_test = test_df.drop(columns=["Class", "Time"])  # Drop 'Time' to match training features
y_test = test_df["Class"]

# --- Load model and scaler ---
model = joblib.load(os.path.join("models", "xgb_fraud_model.pkl"))
scaler = joblib.load(os.path.join("models", "scaler.pkl"))

# --- Scale test data ---
X_test_scaled = scaler.transform(X_test)

# --- Make predictions ---
y_pred = model.predict(X_test_scaled)

# --- Generate metrics ---
report = classification_report(y_test, y_pred, output_dict=True)
conf_matrix = confusion_matrix(y_test, y_pred)

# --- Print to console ---
print("📊 Classification Report:")
print(classification_report(y_test, y_pred))

print("🧮 Confusion Matrix:")
print(conf_matrix)

# --- Save reports ---
os.makedirs("metrics", exist_ok=True)
pd.DataFrame(report).transpose().to_csv("metrics/classification_report.csv")
pd.DataFrame(conf_matrix).to_csv("metrics/confusion_matrix.csv")
