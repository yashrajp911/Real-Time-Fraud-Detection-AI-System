import os
import json
import logging
import requests
import pandas as pd
from datetime import datetime
from kafka import KafkaConsumer
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv(dotenv_path="D:/Project X/fraud_detection_ai/.env")

# ✅ Read values from .env
topic = os.getenv("KAFKA_TOPIC")
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVER").split(",")
API_URL = os.getenv("API_URL")
THRESHOLD = float(os.getenv("THRESHOLD"))
log_file = os.getenv("LOG_FILE")
alert_file_path = os.getenv("ALERT_FILE")

# ✅ Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ✅ Kafka consumer setup
consumer = KafkaConsumer(
    topic,
    bootstrap_servers=bootstrap_servers,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

# ✅ Prediction function
def predict_transaction(transaction):
    try:
        response = requests.post(API_URL, json=transaction)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Prediction failed: {response.status_code} - {response.text}")
    except Exception as e:
        logging.error(f"Error sending request: {e}")
    return None

# ✅ Kafka message consumption
for message in consumer:
    transaction = message.value

    if "Time" in transaction:
        transaction.pop("Time")

    logging.info(f"New transaction: {transaction}")
    prediction = predict_transaction(transaction)

    if prediction:
        log_entry = transaction.copy()
        log_entry["fraud_probability"] = prediction["fraud_probability"]
        log_entry["is_fraud"] = prediction["is_fraud"]
        log_entry["threshold_used"] = THRESHOLD
        log_entry["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 🚨 Alert if fraudulent
        if prediction["is_fraud"]:
            alert_msg = f"🚨 FRAUD ALERT! Amount: ${transaction['Amount']} | Probability: {prediction['fraud_probability']:.4f} | Time: {log_entry['timestamp']}"
            print("\033[91m" + alert_msg + "\033[0m")
            with open(alert_file_path, "a", encoding="utf-8") as alert_file:
                alert_file.write(alert_msg.encode("ascii", "ignore").decode() + "\n")

        # ✅ Append to CSV log
        df = pd.DataFrame([log_entry])
        df.to_csv(log_file, mode='a', header=not os.path.exists(log_file), index=False)

        logging.info(f"Fraud Probability: {prediction['fraud_probability']} | Threshold: {THRESHOLD} | Flagged: {prediction['is_fraud']}")
