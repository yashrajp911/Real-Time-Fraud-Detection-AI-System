import json
import time
import pandas as pd
from kafka import KafkaProducer

data = pd.read_csv("D:/Project X/test_data/test_sample.csv")

#Create kafka producer
producer = KafkaProducer(
    bootstrap_servers = 'localhost:9092',
    value_serializer = lambda x: json.dumps(x).encode('utf-8')
)

topic = 'transactions'

print(f"Streaming {len(data)} transactions...")

for _, row in data.iterrows():
    transaction = row.drop("Class", errors="ignore").to_dict()
    producer.send(topic, value=transaction)
    print(f"Sent: {transaction}")
    time.sleep(1)
    
producer.flush()
print("✅ Done streaming transactions.")