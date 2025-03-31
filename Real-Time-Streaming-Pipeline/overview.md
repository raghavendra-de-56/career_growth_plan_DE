## Real-Time Streaming Pipeline for IoT Data

A real-time streaming pipeline is essential for processing continuous data streams from IoT devices, such as sensors, smart meters, or industrial machines. In this example, we build a real-time IoT streaming pipeline using Apache Spark Structured Streaming and Kafka.

### Architecture of the Real-Time IoT Streaming Pipeline

**Data Source:** IoT devices continuously send data to Kafka topics.

**Ingestion Layer:** Spark Structured Streaming consumes the real-time data from Kafka.

**Processing Layer:** Data is transformed, filtered, and aggregated in real-time.

**Storage Layer:** Processed data is stored in Delta Lake (or another storage).

**Serving Layer:** The results can be sent to dashboards, alerts, or databases.

**Example:** Monitoring temperature and humidity from IoT sensors in a manufacturing plant.

### Kafka Producer: IoT Device Simulation

A Kafka producer simulates IoT devices by sending JSON messages to a Kafka topic.

Kafka Producer Code (Python)
```
from kafka import KafkaProducer
import json
import random
import time

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

iot_device_ids = ["device_1", "device_2", "device_3"]

while True:
    message = {
        "device_id": random.choice(iot_device_ids),
        "temperature": round(random.uniform(20.0, 80.0), 2),
        "humidity": round(random.uniform(30.0, 90.0), 2),
        "timestamp": int(time.time())
    }
    producer.send("iot_topic", message)
    print(f"Sent: {message}")
    time.sleep(2)
```
This script simulates real-time IoT sensor data and sends it to Kafka.

Each message contains device_id, temperature, humidity, and timestamp.

The script runs in a loop, sending messages every 2 seconds.
