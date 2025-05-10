### Scenario: Real-Time Order Processing Platform

Question:
Design a scalable, low-latency system to ingest and process e-commerce orders in real time. Each order must be validated, enriched, persisted, and available for downstream analytics and fraud checks within seconds.

Key Requirements:

Real-time ingestion and processing (under 5 seconds latency)

Idempotent order ingestion

Ability to replay/reprocess events

Schema evolution and audit logs

Scalable to 1M events/minute


Solution Overview:

Ingestion Layer: Apache Kafka (multiple partitions by order ID)

Processing Layer: Spark Structured Streaming with watermarking, schema enforcement

Persistence: Delta Lake (Bronze → Silver → Gold)

Query Layer: Databricks SQL or Delta Sharing

Audit & Replay: Store raw Kafka events in Delta Bronze for replay

Schema Drift Handling: Use Auto Loader + Schema Evolution enabled

Lineage/Governance: Unity Catalog, Delta Live Tables (DLT)
