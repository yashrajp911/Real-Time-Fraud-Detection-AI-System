from fastapi import FastAPI, Query
from pydantic import BaseModel
from datetime import datetime
import joblib
import numpy as np
import os
import logging
import pandas as pd

logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#load model and scaler
model = joblib.load(os.path.join("models","xgb_fraud_model.pkl"))
scaler = joblib.load(os.path.join("models","scaler.pkl"))

app = FastAPI()

class Transaction(BaseModel):
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float
    Amount: float
    
@app.post("/predict")
def predict(data: Transaction, threshold: float = Query(0.5, ge=0.0, le=1.0)):
    input_data = np.array ([[value for value in data.model_dump().values()]])
    input_scaled = scaler.transform(input_data)
    prob = model.predict_proba(input_scaled)[0][1]
    is_fraud = bool(prob > threshold)
    
    logging.info(f"New transaction: {data.model_dump()}")
    logging.info(f"Fraud Probability: {prob:.4f} | Threshold: {threshold} | Flagged: {is_fraud}")
    
    #save to csv
    log_to_csv(data.model_dump(), prob, is_fraud, threshold)
    
    return{
        "fraud_probability": round(float(prob), 4),
        "is_fraud": is_fraud
    }
    
    
def log_to_csv(transaction_dict, prob, is_fraud, threshold):
    log_entry = {
        **transaction_dict,
        "fraud_probability": round(float(prob), 4),
        "is_fraud" : is_fraud,
        "threshold_used" : threshold,
        "timestamp" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    df = pd.DataFrame([log_entry])
    log_file = "prediction_logs.csv"
    
    if not os.path.exists(log_file):
        df.to_csv(log_file, index=False)
    else:
        df.to_csv(log_file, mode='a', header=False, index=False)