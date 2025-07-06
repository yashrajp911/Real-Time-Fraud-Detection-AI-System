import streamlit as st
import pandas as pd
import time
import os
from datetime import datetime

ALERT_LOG_FILE = "fraud_alerts.log"

st.set_page_config(page_title="🚨 Fraud Alert Panel", layout="wide")
st.title("🚨 Fraud Alerts Dashboard")

placeholder = st.empty()

def load_alerts():
    if not os.path.exists(ALERT_LOG_FILE):
        return []

    with open(ALERT_LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        alerts = [line.strip() for line in lines if line.strip()]
    return alerts

def extract_timestamp(alert):
    try:
        parts = alert.split(" | ")
        for part in parts:
            if "Time:" in part:
                return datetime.strptime(part.replace("Time: ", ""), "%Y-%m-%d %H:%M:%S")
    except:
        return None

# Real-time dashboard refresh loop
while True:
    alerts = load_alerts()
    with placeholder.container():
        st.subheader("📣 Recent Fraud Alerts")

        if alerts:
            # Display the 10 most recent alerts
            for alert in reversed(alerts[-10:]):
                st.markdown(f"<div style='color:red;font-weight:bold'>{alert}</div>", unsafe_allow_html=True)

            # Timeline chart of alerts
            timestamps = [extract_timestamp(a) for a in alerts if extract_timestamp(a) is not None]
            if timestamps:
                df = pd.DataFrame({"Alert": 1, "Time": timestamps})
                df = df.set_index("Time").resample("1min").sum().fillna(0)
                st.subheader("📈 Alert Frequency Over Time")
                st.line_chart(df)
        else:
            st.info("No fraud alerts found yet.")

    time.sleep(5)
