from pymongo import MongoClient
from datetime import datetime, timedelta
import random

client = MongoClient("mongodb://localhost:27017/")
db = client["iot"]
collection = db["sensor_readings"]

now = datetime.utcnow()
docs = []

for i in range(500):
    docs.append({
        "sensorId": f"sensor_{random.randint(1,5)}",
        "timestamp": now - timedelta(seconds=i * 10),
        "reading": round(random.uniform(60, 90), 2)
    })

collection.insert_many(docs)
print(f"Inserted {len(docs)} docs")
