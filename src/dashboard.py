import pandas as pd
import streamlit as st
import time
import os 
import seaborn as sns
import matplotlib.pyplot as plt

LOG_FILE = "prediction_logs.csv"

st.set_page_config(page_title="Fraud Detection Dashboard", layout="wide")

st.title("🔍 Real-Time Fraud Detection Dashboard")

placeholder = st.empty()

def load_data():
    if os.path.exists(LOG_FILE):
        return pd.read_csv(LOG_FILE)
    else:
        return pd.DataFrame()

# Live refresh every 5 sec
while True:
    df = load_data()
    with placeholder.container():
        st.subheader("📊 Latest Predictions")
        if not df.empty:
            st.dataframe(df.tail(10), use_container_width=True)
            
            fraud_count = df['is_fraud'].sum()
            total_count = len(df)
            fraud_rate = (fraud_count / total_count) * 100
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Transactions", f"{total_count}")
            col2.metric("Fraudulent", f"{fraud_count}")
            col3.metric("Fraud Rate", f"{fraud_rate:.2f}%")
            
            st.line_chart(df['fraud_probability'].tail(50))
        else:
            st.warning("No prediction logs found.")
        
        # **Your added metrics code starts here**
        if os.path.exists("metrics/classification_report.csv") and os.path.exists("metrics/confusion_matrix.csv"):
            st.subheader("📈 Model Performance (Static Metrics)")

            report_df = pd.read_csv("metrics/classification_report.csv", index_col=0)
            st.dataframe(report_df.style.format(precision=2), use_container_width=True)

            conf_df = pd.read_csv("metrics/confusion_matrix.csv", header=None)

            # Replace NaNs or inf values (just in case)
            conf_df = conf_df.fillna(0)
            conf_df = conf_df.astype(int)

            fig, ax = plt.subplots()
            sns.heatmap(conf_df, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Non-Fraud", "Fraud"], yticklabels=["Non-Fraud", "Fraud"])
            ax.set_xlabel("Predicted")
            ax.set_ylabel("Actual")
            st.pyplot(fig)

        else:
            st.warning("Model metrics not found. Please run model_metrics.py.")
        # **End of added metrics code**

    time.sleep(5)
