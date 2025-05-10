### Why Do We Need These Architectures?

Modern systems deal with:

Huge volumes of data (e.g., IoT, logs, transactions, etc.)

The need for real-time analytics (fraud detection, recommendation engines)

The requirement for accurate batch processing (monthly reports, data lakes)

Traditional architectures struggled to meet both real-time and batch needs efficiently — hence, Lambda and Kappa were introduced.

<img width="656" alt="image" src="https://github.com/user-attachments/assets/1dc1c43e-f8b8-4d49-81cf-ea3f84e5c7b7" />

### Lambda Architecture (LA)

Lambda was proposed by Nathan Marz (creator of Apache Storm). It aims to provide:

Scalable

Fault-tolerant

Real-time + batch data processing

#### Lambda Layers

##### Batch Layer

Stores all incoming data (immutable, append-only)

Performs heavy computation and generates batch views

Example: Hadoop, Apache Spark

##### Speed Layer

Processes only recent data (in real-time)

Complements the latency of the batch layer

Example: Apache Storm, Spark Streaming, Kafka Streams

##### Serving Layer

Merges batch and real-time views

Responds to queries

Example: Apache Druid, Elasticsearch

How It Works (Flow):
```
Incoming Data → HDFS (Batch Layer)
              → Kafka → Storm (Speed Layer)
Batch Layer → Spark Job → Batch View
Speed Layer → Stream Process → Real-time View
Both Views → Serving Layer → Queries
```
Pros:

Combines accuracy (batch) and speed (real-time)

Scalable and fault-tolerant

Cons:

Code duplication: Business logic needs to be written twice (batch + real-time)

Complexity: Managing two code paths and data flows

### Kappa Architecture (KA)

Proposed by Jay Kreps (creator of Kafka), Kappa simplifies data processing by eliminating batch processing entirely.

Core Principle:

> Treat all data as a stream. If you need to reprocess, just replay the stream.

##### Kappa Flow:
```
Incoming Data → Kafka
Kafka → Stream Processor (Flink, Spark Streaming, Kafka Streams)
Stream Processor → Materialized Views or Data Lake
```
##### Key Components:

Kafka: Stores immutable event logs (acts as both buffer and storage)

Stream Processor: Processes data in real-time

Output Stores: Druid, Cassandra, Delta Lake, etc.

##### Pros:

Simpler architecture (only one processing pipeline)

No code duplication

Easier reprocessing (via stream replay)

##### Cons:

Still maturing vs batch (handling late data, large aggregates)

Requires accurate and robust streaming infrastructure

##### When to Use Which?

Criteria	Lambda	Kappa

Code Duplication	High (batch + stream)	Low (single stream code path)

Complexity	High	Moderate

Real-Time Requirement	Medium to High	High

Reprocessing Needs	Limited, via batch	Replay entire stream

Use Cases	Fraud detection + reporting	IoT, real-time metrics, ML

##### Real-World Example: IoT in Retail

###### Lambda:

Devices send sensor data → HDFS & Kafka

Batch jobs process daily aggregates (sales, temperature, etc.)

Stream layer triggers real-time alerts for anomalies

Serving layer merges both for dashboards

###### Kappa:

IoT devices send data to Kafka

Kafka Streams processes real-time stats

Druid used for querying data

To reprocess logic: deploy a new stream job and replay Kafka

##### Code Illustration (Kappa-style in PySpark Structured Streaming)

```
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

spark = SparkSession.builder \
    .appName("IoT Kappa Pipeline") \
    .getOrCreate()

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:9092") \
    .option("subscribe", "iot-topic") \
    .load()

# Transform
json_df = df.selectExpr("CAST(value AS STRING) as message")

# Enrich/Parse JSON
parsed_df = json_df.selectExpr("from_json(message, 'device_id STRING, temp DOUBLE, ts TIMESTAMP') as data") \
    .select("data.*")

# Write to Delta Lake
query = parsed_df.writeStream \
    .format("delta") \
    .option("checkpointLocation", "/checkpoints/iot") \
    .outputMode("append") \
    .start("/delta/iot_data")

```

###### Summary

![image](https://github.com/user-attachments/assets/8e543340-5da1-406c-a8dc-1a5502318f45)


