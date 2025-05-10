#### 1. Real-Time Ingestion with Kafka/Spark Structured Streaming

Concept:

Kafka is a distributed log system. Spark Structured Streaming can read from Kafka topics in real time, making it ideal for micro-batch processing.

Code:
````
df_kafka = (spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "broker1:9092")
    .option("subscribe", "orders_topic")
    .option("startingOffsets", "latest")
    .load())

df_parsed = df_kafka.selectExpr("CAST(value AS STRING)")
````

#### 2. Delta Lake Internals in Streaming Context

Concept:

Delta Lake supports ACID transactions and schema enforcement. In streaming, it ensures atomic writes, high throughput, and consistency for downstream reads.

Key Internals:

Transaction Logs: _delta_log/

Schema Enforcement: Rejects incompatible schema writes

Streaming Append Mode: Adds new rows incrementally

Change Data Feed (CDF): Exposes row-level changes in Delta tables

#### 3. Databricks Autoloader for Streaming Ingestion

Concept:

Autoloader is a Databricks-native utility that incrementally ingests files from cloud storage with high scalability and schema evolution support.

Code:
```
df_auto = (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .load("/mnt/raw/orders/"))

df_auto.writeStream \
    .format("delta") \
    .option("checkpointLocation", "/mnt/chk/orders/") \
    .start("/mnt/delta/orders/")
````

---

#### 4. Delta Table Streaming Reads & Writes

Concept:

Delta tables can be used in both read and write streaming scenarios. This enables building streaming ETL pipelines.

Code – Streaming Write:
```
df_transformed.writeStream \
    .format("delta") \
    .outputMode("append") \
    .option("checkpointLocation", "/mnt/chk/enriched_orders/") \
    .start("/mnt/delta/enriched_orders/")
```
Code – Streaming Read:
```
df_delta_stream = (spark.readStream
    .format("delta")
    .load("/mnt/delta/enriched_orders/"))
```

#### 5. Watermarking, Late Data Handling

Concept:

Watermarking tells Spark how late data can be.

Late records beyond watermark are dropped.

Helps manage state and prevent OOM issues.


Code:
```
from pyspark.sql.functions import window, to_timestamp

df = df.withColumn("event_time", to_timestamp("order_time"))

aggregated = df.withWatermark("event_time", "10 minutes") \
    .groupBy(window("event_time", "5 minutes")) \
    .count()
```

6. Delta Lake Change Data Feed (CDF)

Concept:

Delta Lake CDF allows consumers to query changed rows from Delta tables using table_changes.

Enable CDF:
```
ALTER TABLE orders SET TBLPROPERTIES (delta.enableChangeDataFeed = true);
```
Read Changed Rows:
```
SELECT * FROM table_changes('orders', '2024-05-01');
```

#### 7. Querying Streams with Databricks SQL

Concept:

Once streaming writes data to Delta tables, Databricks SQL can query them in real time.

Example Query:
```
SELECT region, COUNT(*) as order_count
FROM orders
WHERE order_time >= current_date()
GROUP BY region;
```

#### 8. Building Real-Time Dashboards on Delta Tables

Concept:

Use Databricks SQL to create visual dashboards with auto-refresh capabilities. Link charts to orders Delta table.

Steps:

Create visualization → Bar Chart → COUNT(order_id) by region

Add filters → WHERE order_time >= NOW() - interval 1 hour

Enable auto-refresh

#### 9. Optimizing and Monitoring Streaming Jobs

Concept:

OptimizeWrite: Reduces small files

Auto Compaction: Merges files

Streaming UI: Shows batch duration, watermark progress, input rows


Config:
```
spark.conf.set("spark.databricks.delta.optimizeWrite.enabled", "true")
spark.conf.set("spark.databricks.delta.autoCompact.enabled", "true")
```

#### 10. Failover, Recovery, and Idempotency in Streaming Pipelines

Concept:

Checkpoints ensure recovery.

Delta writes are idempotent.

Deduplication can be added based on unique IDs and event time.

Code with Deduplication:
```
df_deduped = df.dropDuplicates(["order_id", "order_time"])

df_deduped.writeStream \
    .format("delta") \
    .option("checkpointLocation", "/mnt/chk/deduped/") \
    .start("/mnt/delta/orders_deduped/")
```
