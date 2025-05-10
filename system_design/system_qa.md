#### 1. How would you design a real-time data pipeline using Kafka and Delta Lake in Databricks?

Answer:

Use Kafka as the event ingestion layer.

Use Structured Streaming in Databricks to consume Kafka messages.

Transform and enrich data using Spark DataFrame APIs.

Write the output to Delta Lake, using append mode for ingestion and merge mode for deduplication or CDC patterns.

Maintain checkpointing for exactly-once semantics.

Optionally, trigger alerts using Databricks SQL or integrate with ML models for real-time predictions.


#### 2. How do you handle schema evolution in real-time pipelines?

Answer:

Delta Lake supports schema evolution using mergeSchema = true.

Use a schema registry like Confluent Schema Registry to validate versions.

Add logic to handle backward/forward compatibility.

Use structured streaming’s from_json with schema_of_json or explicitly defined schemas.

Monitor schema drift and raise alerts when new fields are detected.

#### 3. How does Delta Lake ensure reliability in real-time pipelines?

Answer:

ACID transactions ensure consistency even in concurrent writes.

Time Travel allows rollback and auditing.

Data versioning enables reproducibility.

Built-in schema enforcement and evolution prevent corrupt data.

It supports checkpointing and exactly-once guarantees when used with Structured Streaming.

#### 4. What are the differences between append-only and upsert (merge) modes in real-time streaming?

Answer:

Mode	Use Case

Append	When new data is always added (e.g., logs)

Merge/Upsert	When data can be updated/deleted (e.g., CDC)

Use MERGE INTO in Delta Lake for upserts using a key column.

Append mode is faster but doesn’t handle duplicates or updates.

#### 5. Explain watermarks and late data handling in Spark Structured Streaming.

Answer:

Watermarks specify how long to wait for late data.

Syntax: withWatermark("timestamp", "10 minutes")

Helps manage state size and windowing.

Late events after the watermark threshold are discarded.

#### 6. How do you optimize Delta Lake tables for performance?

Answer:

Use OPTIMIZE command to compact small files.

Use ZORDER BY for better data skipping.

Periodically vacuum unused files using VACUUM.

Partition the table on high-cardinality columns wisely.

#### 7. What is the role of Databricks SQL in real-time pipelines?

Answer:

Allows SQL-based access to Delta Tables in near real-time.

Can power dashboards and alerts.

Supports materialized views or live dashboards using Databricks SQL Alerts.

Enables self-service analytics for non-engineers.

#### 8. How do you ensure end-to-end data lineage in a real-time pipeline?

Answer:

Use Unity Catalog to track table dependencies and schema versions.

Integrate with OpenLineage or Databricks lineage features.

Capture metadata in checkpoints and logs.

Use naming conventions and version control for notebooks.

#### 9. How do you debug failures in a streaming pipeline in Databricks?

Answer:

Use Streaming Query Listener to track metrics and failures.

Check checkpoint logs for progress or corruption.

Enable debug logs and try-catch blocks.

Validate Kafka offsets and connectivity.

Use query.lastProgress and describeHistory() for Delta operations.

#### 10. How would you handle exactly-once processing in a Kafka-Spark-Delta pipeline?

Answer:

Enable checkpointing and idempotent writes.

Use Kafka offsets for deterministic processing.

Use Delta Lake’s upsert patterns to handle duplicates.

Consider deduplication logic based on event_id or composite keys.

### Real-Time Streaming (Kafka/Spark Structured Streaming)

##### Q1: How does Kafka ensure message durability and fault tolerance?
A: Kafka persists messages to disk and replicates data across brokers. It uses an acknowledgment system (acks) to confirm delivery to followers before confirming to producers.

##### Q2: How do you handle late-arriving data in Spark Structured Streaming?
A: By using watermarking to define how late data can arrive and still be aggregated, e.g.:
```
df.withWatermark("event_time", "10 minutes")
   .groupBy(window("event_time", "5 minutes"))
   .agg(count("*"))
```
##### Q3: What are the guarantees provided by Spark Structured Streaming?
A: It provides exactly-once, at-least-once, and at-most-once delivery semantics depending on sink and configuration.

### Delta Lake

##### Q4: What are Delta Lake's key features?
A: ACID transactions, schema enforcement and evolution, time travel, data versioning, and unified batch and stream processing.

##### Q5: How does Delta Lake support time travel and versioning?
A: Each write to a Delta table creates a new version (stored as a transaction log). You can query past versions:
```
SELECT * FROM delta./path/to/table VERSION AS OF 10
```
##### Q6: How is schema enforcement handled in Delta?
A: Delta fails writes when schema mismatches unless mergeSchema is enabled:
```
df.write.option("mergeSchema", "true").format("delta").mode("append").save()
```

### Databricks SQL

##### Q7: What are common performance optimizations in Databricks SQL?
A:

Use Z-Ordering for better file pruning.

Use OPTIMIZE and VACUUM regularly.

Filter using partition columns.
```
OPTIMIZE delta./path ZORDER BY (user_id)
```
##### Q8: How does Unity Catalog enhance governance in Databricks SQL?
A: Provides centralized access control, column-level lineage, audit logs, and data classification across all workspaces.

End-to-End Streaming Project Interview Questions

##### Q9: Describe an end-to-end Kafka to Delta pipeline architecture.
A:
```
Kafka → Spark Structured Streaming → Transform → Write to Delta Table → Query with Databricks SQL.
```
Metadata managed with Unity Catalog, orchestrated via Airflow.

##### Q10: How do you ensure fault-tolerance and scalability in a real-time pipeline?
A:

Enable checkpointing in Spark Streaming.

Use Kafka consumer groups for parallel processing.

Store intermediate state in Delta or external key-value stores.

##### Q11: How do you handle schema drift in real-time pipelines?
A: Implement schema inference + validation in ingestion, use schema evolution in Delta Lake, log anomalies for review.


