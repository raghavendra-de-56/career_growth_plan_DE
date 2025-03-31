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

### Spark Structured Streaming: Consuming IoT Data from Kafka

We now consume and process the real-time IoT data using Spark Structured Streaming.

Spark Structured Streaming Code
```
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
from pyspark.sql.functions import from_json, col

# Define schema for IoT data
iot_schema = StructType([
    StructField("device_id", StringType(), True),
    StructField("temperature", DoubleType(), True),
    StructField("humidity", DoubleType(), True),
    StructField("timestamp", IntegerType(), True)
])

# Read data from Kafka topic
df_stream = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "iot_topic")
    .option("startingOffsets", "latest")  # Read only new messages
    .load()
)

# Deserialize JSON messages
df_parsed = df_stream.selectExpr("CAST(value AS STRING) as json").select(from_json(col("json"), iot_schema).alias("data")).select("data.*")

# Filter high-temperature events (Example: Alert if temperature > 70°C)
df_alerts = df_parsed.filter(df_parsed["temperature"] > 70)

# Write alerts to console in real time
df_alerts.writeStream.outputMode("append").format("console").start()
```
Key Features:

✅ Reads data from Kafka in real time.

✅ Parses the JSON payload and extracts relevant fields.

✅ Filters high-temperature events (above 70°C).

✅ Streams alerts to the console for monitoring.

### Writing Processed Data to Delta Lake

For long-term storage and historical analysis, we write the processed data to Delta Lake.

Writing to Delta Lake
```
df_parsed.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/tmp/delta_checkpoint/") \
    .start("/mnt/delta/iot_data/")
```
Delta Lake ensures ACID transactions for streaming data.

Checkpoints help with fault tolerance and recovery.

Scales for large-scale IoT datasets.

### Real-Time Dashboard with Apache Spark & Databricks

For real-time visualization, we can use Databricks SQL or Grafana.

Databricks SQL Query to Analyze IoT Data
```
SELECT 
    device_id, 
    AVG(temperature) AS avg_temp, 
    MAX(humidity) AS max_humidity 
FROM delta./mnt/delta/iot_data/ 
GROUP BY device_id;
```
Queries stored IoT data for insights.

Detects temperature spikes and abnormal patterns.

### Advanced Use Cases for Interviews

(a) Anomaly Detection in IoT Data

Use machine learning models in Spark to detect anomalies in real-time.

Example: Identify faulty sensors using Z-score or Isolation Forest.

```
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans

# Convert IoT data into feature vectors
assembler = VectorAssembler(inputCols=["temperature", "humidity"], outputCol="features")
df_features = assembler.transform(df_parsed)

# Train K-Means model to detect anomalies
kmeans = KMeans(k=2, featuresCol="features", predictionCol="cluster")
model = kmeans.fit(df_features)

# Detect anomalous sensor readings
df_anomalies = model.transform(df_features).filter("cluster = 1")
df_anomalies.writeStream.format("console").start()
```
(b) Dynamic Scaling for High-Volume IoT Data

Auto-scale Kafka consumers based on load.

Use Apache Flink or Kubernetes for high-throughput scenarios.

### Summary

✅ Built a real-time Spark Streaming pipeline for IoT sensor data.

✅ Connected Spark with Kafka for real-time ingestion.

✅ Stored processed data in Delta Lake for historical analysis.

✅ Implemented real-world use cases like anomaly detection and alerting.

