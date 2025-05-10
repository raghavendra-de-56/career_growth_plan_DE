### Design a real-time fraud detection system.

Key Requirements:

Sub-second latency

Rule-based and ML-based anomaly detection

Stream ingestion, processing, storage, and alerting

Design Components:

Kafka: ingest payment transaction streams

Spark Structured Streaming: apply rules (e.g., transactions > threshold, geo mismatch)

Delta Lake Bronze/Silver: for storage and audits

MLflow or Feature Store: manage real-time fraud detection models

Alert System: push notifications (Slack, PagerDuty, email)
