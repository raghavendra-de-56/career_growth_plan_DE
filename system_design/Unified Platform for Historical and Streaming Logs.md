### Unified Platform for Historical and Streaming Logs

Question:
Design a system to ingest and analyze application logs in real-time and also provide historical querying for debugging and analytics.

Answer:

Use Kafka (or Kinesis) for real-time log ingestion

Stream logs via Spark Structured Streaming into Delta Lake Bronze

Delta Time Travel + Versioning provides historical log querying

Delta Lake Merge API helps enrich logs with metadata or correlate with deployment timelines

Databricks SQL and BI tools (e.g., Power BI, Tableau) query the Gold Layer

Partition logs by service/date to optimize query performance
