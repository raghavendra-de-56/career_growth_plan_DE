### How would you design a real-time streaming pipeline using Kafka and Delta Lake?

Answer:

Architecture Overview:

1. Source Systems (IoT, Weblogs, Sensors) generate data continuously.

2. Kafka ingests and buffers real-time data streams.

3. Spark Structured Streaming consumes Kafka topics in micro-batches.

4. Transformations (parsing, validation, enrichment) are applied in Spark.

5. Delta Lake Bronze Layer stores raw ingested data.

6. Delta Silver Layer applies business logic, deduplication, and joins with dimensions.

7. Delta Gold Layer provides aggregated facts for downstream consumption via Databricks SQL or dashboards.


Code Snippet (Spark Structured Streaming with Delta Lake):
```
from pyspark.sql.types import StructType, StringType, DoubleType
from pyspark.sql.functions import from_json, col

# Define Kafka input schema
schema = StructType().add("device_id", StringType()).add("temperature", DoubleType())

df = (spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "kafka:9092")
        .option("subscribe", "iot_topic")
        .load())

# Parse JSON
parsed_df = df.selectExpr("CAST(value AS STRING)").select(from_json("value", schema).alias("data")).select("data.*")

# Write to Bronze Delta Table
parsed_df.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/mnt/checkpoints/bronze") \
    .start("/mnt/delta/bronze")
```

### What are the key challenges in real-time systems and how do you handle them?

Key Challenges & Solutions: 
|------------|---------|
| Challenge | Solution | 
|----------|----------| 
| Data Skew | Use partitioning wisely and broadcast joins. |
| Late Arriving Data | Use watermarking in Spark Structured Streaming. | 
| Schema Drift | Enable schema evolution and implement drift detection using expectations. | 
| Exactly-once Processing | Use checkpointing and idempotent writes in Delta Lake. |
