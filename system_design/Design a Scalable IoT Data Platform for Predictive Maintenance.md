### Design a Scalable IoT Data Platform for Predictive Maintenance

Prompt:

> Millions of devices emit telemetry every few seconds. You must build a system that enables predictive maintenance using both historical and real-time insights.


Key Points to Cover:

Ingest sensor data via Kafka with protobuf schemas.

Use Kappa architecture with Flink/Spark Streaming.

Delta Lake bronze-silver-gold pipeline for real-time + historical processing.

Train ML models using time-series features.

Orchestrate with Airflow/Databricks Workflows.
