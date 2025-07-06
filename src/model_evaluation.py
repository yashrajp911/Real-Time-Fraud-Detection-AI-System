import joblib
import pandas as pd
import os
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler

test_df = pd.read_csv("D:/Project X/test_data/test_sample.csv")

X_test = test_df.drop("Class", axis=1)
y_test = test_df["Class"]

#load model and scaler
model = joblib.load(os.path.join("models","xgb_fraud_model.pkl"))
scaler = joblib.load(os.path.join("models","scaler.pkl"))

# Scale the test data
X_test = X_test.drop(columns=["Time"])
X_test_scaled = scaler.transform(X_test)

# Predict
y_pred = model.predict(X_test_scaled)

# Report
print("📊 Classification Report:")
print(classification_report(y_test, y_pred))

print("🧮 Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))