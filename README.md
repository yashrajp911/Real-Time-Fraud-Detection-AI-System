🚨 Real-Time Fraud Detection AI System

A full-fledged real-time fraud detection pipeline built using machine learning, FastAPI, Apache Kafka, and Streamlit. This project monitors transaction data in real-time, detects fraudulent behavior, and provides instant visual alerts via a dashboard.

---

📌 Features

- ML Model trained on the Kaggle Credit Card Fraud Dataset (XGBoost)
- FastAPI for real-time prediction serving
- Kafka Producer/Consumer to stream transactions
- Streamlit Dashboard for live monitoring
- Fraud Detection Alerts in terminal + log files
- Organized with `.env` and modular folder structure
- Optional Docker setup for containerized deployment

---

📂 Project Structure

FRAUD_DETECTION_AI/
├── .venv/                  Virtual environment
├── app/                   FastAPI application
│   └── main.py
├── src/                   Core pipeline scripts
│   ├── producer.py
│   ├── consumer.py
│   ├── model_evaluation.py
│   ├── dashboard.py
│   └── alert_dashboard.py
├── models/                Trained models & scalers
│   ├── xgb_fraud_model.pkl
│   └── scaler.pkl
├── metrics/               Evaluation reports
│   ├── classification_report.csv
│   └── confusion_matrix.csv
├── logs/                  Logs and alerts
│   ├── alerts.log
│   ├── fraud_alerts.log
│   └── prediction_logs.csv
├── notebooks/             Jupyter notebooks
│   └── credit_fraud.ipynb
├── docker-compose.yml     Docker config (Kafka + Zookeeper)
├── requirements.txt       Python dependencies
├── .env                   Environment variables
├── README.md              Project documentation
└── LICENSE                License info

---

🚀 How It Works

1. Producer streams one transaction at a time from a dataset to Kafka
2. Consumer listens to Kafka and sends each transaction to the FastAPI model server
3. FastAPI returns fraud probability
4. Consumer logs the prediction and triggers fraud alerts if necessary
5. Streamlit Dashboard displays live fraud detection metrics and graphs

---

🧪 Tech Stack

- Python
- scikit-learn & XGBoost
- Apache Kafka
- FastAPI
- Streamlit
- Docker (optional)
- Pandas, Requests, Logging

---

🛠️ Setup Instructions

1. Install Dependencies

pip install -r requirements.txt

2. Configure `.env`

KAFKA_BOOTSTRAP_SERVER=localhost:9092
KAFKA_TOPIC=transactions
API_URL=http://localhost:8000/predict
THRESHOLD=0.3
LOG_FILE=logs/prediction_logs.csv
ALERT_FILE=logs/fraud_alerts.log

3. Run Components

Start Kafka:
docker compose up -d

Start FastAPI:
cd app
uvicorn main:app --reload

Start Producer:
python src/producer.py

Start Consumer:
python src/consumer.py

Launch Dashboard:
streamlit run src/dashboard.py

---

📈 Example Output

- 🚨 Terminal alerts for frauds
- 📉 Dashboard showing fraud rate & recent predictions
- 🗂️ `prediction_logs.csv` storing transaction logs

---

🧠 ML Model Info

- Model: XGBoost Classifier
- Trained on: Kaggle Credit Card Fraud Dataset
- Scaler: StandardScaler
- Metrics: Accuracy, Precision, Recall, F1-score, Confusion Matrix

---

🧪 Evaluation

- Model tested on holdout dataset
- 100% Precision and Recall (Demo Mode)
- Confusion Matrix and report saved under `/metrics`

---

🔒 License

MIT License © 2025 Yashraj Pawar
