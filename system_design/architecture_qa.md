#### 1. Q: How would you design a real-time data pipeline for IoT sensor data in a large-scale system?

A:

Architecture Components:

Ingestion: Kafka or AWS Kinesis.

Stream Processing: Spark Structured Streaming or Flink.

Storage: Delta Lake (bronze/silver/gold layers).

Serving Layer: Databricks SQL / BI tools.

Monitoring: Datadog, Prometheus, or built-in Spark metrics.

Key Design Considerations:

High-throughput Kafka partitions and replication.

Schema enforcement and evolution with Delta Lake.

Watermarking and windowing for event-time processing.

Time travel and auditability with Delta Lake versioning.

Idempotent writes and exactly-once guarantees.

#### 2. Q: What are the key differences between Lambda and Kappa architectures? When would you use each?

A:

Feature	Lambda Architecture	Kappa Architecture

Layers	Batch + Real-time	Single (Stream)

Codebase	Separate for batch and stream	Unified codebase

Use Case	Complex historical reprocessing	Simple streaming use cases

Complexity	High	Lower

Reprocessing	Easy (Batch Layer)	Re-ingest through stream

Use Lambda when: You need batch precision + real-time insights (e.g., historical corrections).

Use Kappa when: Stream processing is enough and simplicity is preferred (e.g., monitoring apps).


#### 3. Q: How do you ensure fault-tolerance and exactly-once semantics in a Spark Structured Streaming pipeline?

A:

Checkpointing: Store offsets and metadata in a fault-tolerant store (e.g., S3, DBFS).

Idempotent Writes: Use merge (MERGE INTO) instead of append to avoid duplicates.

Delta Lake: Supports ACID transactions and schema evolution.

Output Modes: Use append or update depending on business logic.

```
df.writeStream \
  .format("delta") \
  .option("checkpointLocation", "/mnt/checkpoints") \
  .start("/mnt/delta/silver_layer")
```

#### 4. Q: What is your approach to building a medallion architecture in Databricks for streaming data?

A:

Bronze Layer (raw ingestion):

Store Kafka-structured data as-is.

Retain all metadata and logs.

Silver Layer (cleansed and structured):

Parse JSON fields, enrich with lookup tables.

Deduplicate and handle schema drift.

Gold Layer (aggregated for business):

Real-time aggregations, KPIs, and ready-to-serve dimensions.

Benefits:

Clear separation of raw vs business data.

Supports reprocessing, auditing, time travel.

Ideal for schema evolution and traceability.

#### 5. Q: What design strategies would you apply for scalable real-time analytics in a retail or IoT environment?

A:

Partitioning Strategy: Partition data in Delta by time and device ID.

Auto Load Balancing: Kafka topic with multiple partitions.

Latency vs Throughput: Tune batch size and trigger interval.

Observability: Use Delta Lake’s audit logs + Spark metrics.

Schema Management: Central schema registry or Unity Catalog.

#### 6. Q: How does Databricks SQL help in real-time decision-making pipelines?

A:

Query real-time Delta tables using standard SQL.

Schedule dashboards and queries for BI teams.

Use STREAMING LIVE TABLES for declarative pipelines.

Supports Materialized Views, Lakehouse Federation, and Time Travel.

```
SELECT device_id, AVG(temp)
FROM delta./mnt/delta/silver
WHERE timestamp > current_timestamp() - INTERVAL 5 MINUTES
GROUP BY device_id;
```

