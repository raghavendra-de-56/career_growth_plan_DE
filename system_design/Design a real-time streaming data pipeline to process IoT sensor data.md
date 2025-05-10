### Design a real-time streaming data pipeline to process IoT sensor data in Databricks using Kafka and Delta Lake. How would you ensure scalability, reliability, and low latency?

Answer:

1. High-Level Architecture:
   
```
[ IoT Devices ] 
     |
     v
[ Kafka Topic (Raw Events) ] 
     |
     v
[ Databricks Structured Streaming Job ]
     |
     v
[ Bronze Delta Table (Raw Layer) ]
     |
     v
[ Silver Delta Table (Cleaned/Transformed) ]
     |
     v
[ Gold Delta Table (Aggregated) ]
     |
     v
[ Dashboard / Alerting ]
```

2. Key Components:

Kafka: Acts as a buffer and decouples producers and consumers. Topics partitioned based on device type/location for scalability.

Databricks Structured Streaming: Reads Kafka stream using readStream, applies transformation logic (parsing, validation, enrichment).

Delta Lake (Medallion Architecture):

Bronze: Raw ingest from Kafka.

Silver: Cleansed and enriched with device metadata.

Gold: Aggregated values like hourly average temperature, anomaly counts.


3. Key Design Considerations:

Scalability:

Use Kafka partitioning + Databricks autoscaling clusters.

Separate workloads: ingestion vs transformation.


Reliability:

Delta’s ACID guarantees.

Kafka offsets committed to checkpoint location.


Low Latency:

Trigger: trigger(availableNow=True) or trigger(processingTime="30 seconds").

4. Code Snippet in PySpark (Databricks):
   
```
# Read from Kafka
df_raw = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "broker1:9092")
    .option("subscribe", "iot_sensors")
    .option("startingOffsets", "latest")
    .load()
)

# Parse JSON payload
df_parsed = (
    df_raw.selectExpr("CAST(value AS STRING) as json")
    .select(from_json(col("json"), schema).alias("data"))
    .select("data.*")
)

# Write to Bronze table
df_parsed.writeStream \
    .format("delta") \
    .option("checkpointLocation", "/mnt/checkpoints/iot_bronze") \
    .outputMode("append") \
    .table("iot_bronze")
```
