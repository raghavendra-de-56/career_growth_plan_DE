## Production-Grade Data Architecture

A production-grade data architecture is a system built to reliably handle real-time, large-scale, business-critical data. It integrates ingestion, processing, storage, access control, governance, lineage, observability, and orchestration — all with reliability, scalability, and maintainability in mind.

## Architectural Layers

### Ingestion Layer

Batch: SFTP, APIs, CDC from RDS/Postgres/MySQL

Streaming: Kafka, Kinesis, MQTT (for IoT), Azure Event Hub

Tools: Apache NiFi, Kafka Connect, AWS Glue, Spark Structured Streaming

### Processing Layer

Raw → Bronze: Store raw data for traceability

Bronze → Silver: Clean and standardize

Silver → Gold: Aggregate or join for reporting/ML

Technologies: PySpark, Spark Structured Streaming, Delta Lake, dbt, Pandas for light workloads

### Storage Layer

Data Lakehouse: Delta Lake, Iceberg, or Hudi on top of cloud object stores

Warehouse: Snowflake, BigQuery, Redshift for ad-hoc querying

Catalogs: Unity Catalog, Glue Catalog, Hive Metastore

### Metadata & Governance Layer

Tools: Unity Catalog, Amundsen, DataHub, Apache Atlas

Features: Column-level lineage, tags, classifications, sensitivity levels

### Orchestration & Workflow Layer

Use: Schedule pipelines, manage dependencies, retry on failure

Tools: Airflow, Dagster, Prefect, Databricks Workflows, AWS Step Functions

### Observability & Quality Layer

Monitoring: Prometheus, Grafana, ELK Stack

Data Quality: Great Expectations, Deequ, Soda Core

Alerting: PagerDuty, Slack alerts on SLA misses

## Real-World Scenario: IoT + Supply Chain Pipeline

Imagine you're designing a production system at Nike that ingests temperature & humidity data from thousands of sensors in warehouses across the globe, and feeds that into a planning system.

### Architecture Overview

Source: IoT devices send messages every 5 seconds

Ingestion: Kafka → Spark Structured Streaming

### Processing:

Bronze: Raw JSON from sensors

Silver: Parsed, validated schema with missing values flagged

Gold: Hourly aggregates by region

Storage: Delta Lake on S3 + Snowflake for downstream planners

Lineage & Metadata: Unity Catalog + Delta logs + custom tags

Orchestration: Databricks Workflows triggers hourly aggregations and model scoring

Governance: Access to data segmented by region, with audit logs enabled

Observability: Alert if more than 10% of devices fail to report in a time window

## Here’s how everything fits together:

```
[IoT Devices]
                |
            [Kafka/Kinesis]
                |
         [Raw Zone] -> Orchestrated via Airflow/Workflows
                |
         [Quality Checks] (rule-based filters)
                |
         [Transform/Enrich]
                |
         [Feature Store / Analytics Layer]
                |
         [Dashboards / ML models]

        +---------------------------------------+
        |   Governance Layer: Unity Catalog     |
        |   - RBAC, Auditing, Data Tags         |
        |   - Lineage, Discovery, Classification|
        +---------------------------------------+
```

## Simulating Raw IoT Data Ingestion

### Concept:
This involves ingesting data from IoT devices (sensors, GPS, thermostats, etc.) in near-real time or batch mode.

### Real-World Example:
Factory machines streaming temperature, vibration, and humidity every few seconds into a lakehouse.

### Key Points:

Device ID, timestamp, status, and telemetry values.

Formats: JSON, Parquet, CSV.

Ingestion tools: Kafka, Kinesis, Azure IoT Hub, or directly via batch jobs.

### PySpark Example:
```
from pyspark.sql import Row
import random
from datetime import datetime

now = datetime.utcnow().isoformat()
data = [Row(device_id=f"device_{i%5}", temperature=random.randint(15, 100), ts=now) for i in range(100)]
df = spark.createDataFrame(data)
df.write.format("delta").mode("overwrite").save("/tmp/iot/raw")
```

## Data Quality Checks (Great Expectations or PySpark)

### Concept:
You want to prevent "bad data" (nulls, out-of-range values, malformed formats) from polluting your downstream pipelines.

### Real-World Example:
A temp sensor sending 9999 as a reading (faulty), or a missing device_id.

### Validations You Can Apply:

No nulls in critical fields.

Ranges: temperature between -40 and 150.

Enum values: status in ("active", "idle", "faulty").


### PySpark Example:
```
df = spark.read.format("delta").load("/tmp/iot/raw")
df_valid = df.filter("temperature >= 0 and temperature <= 100 and device_id IS NOT NULL")
df_invalid = df.subtract(df_valid)
```

## Data Transformation & Enrichment

### Concept:
Refining raw data to make it usable—adding computed fields, cleaning, or normalizing it.

### Real-World Example:

Converting Fahrenheit to Celsius.

Deriving an alert column if temperature > 90°F.

Joining with device metadata.

### PySpark Example:
```
df_transformed = df_valid.withColumn("temp_celsius", ((col("temperature") - 32) * 5 / 9).cast("float")) \
                         .withColumn("alert", when(col("temperature") > 90, lit(True)).otherwise(lit(False)))
```

## Unity Catalog & Governance

### Concept:
Unity Catalog (Databricks) allows central management of access control, data classification, and lineage.

### Real-World Example:

Only managers can access salary column.

Tagging PII columns for compliance.

### Things to Implement:

Table registration.

RBAC using groups and Unity Catalog roles.

Tags: PII, sensitive, internal.

Column-level security.

### SQL Example:
```
GRANT SELECT ON TABLE iot_data TO iot_readers;
ALTER TABLE iot_data ALTER COLUMN device_id SET TAGS ('pii' = 'true');
```

## Metadata & Lineage

### Concept:
Track how datasets and fields are transformed across your pipelines. Helps with debugging, auditing, and compliance.

### Real-World Example:

A field alert is derived from temperature.

This field appears in 5 downstream tables and dashboards.

### Tools:

Unity Catalog Lineage.

DataHub, OpenMetadata, Collibra.

Databricks: Lineage is auto-captured and visualized in the Unity Catalog.

## Orchestration with Airflow or Databricks Workflows

### Concept:
Manage the execution of your jobs in order (with dependencies, retries, alerts).

### Real-World Example:

```
Raw ingestion job -> Quality check -> Transformation -> Notify via Slack.
```
```
Databricks Workflow JSON:

{
  "tasks": [
    {"task_key": "ingest", "notebook_path": "/ingest"},
    {"task_key": "validate", "depends_on": ["ingest"], "notebook_path": "/validate"},
    {"task_key": "transform", "depends_on": ["validate"], "notebook_path": "/transform"}
  ]
}
```
### Airflow DAG Skeleton:
```
from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator

with DAG("iot_pipeline", schedule_interval="@hourly", start_date=datetime(2024, 1, 1)) as dag:
    ingest = DatabricksSubmitRunOperator(...)
    validate = DatabricksSubmitRunOperator(...)
    transform = DatabricksSubmitRunOperator(...)

    ingest >> validate >> transform

```
## Principles of Production-Grade Data Architecture

1. Modularity: Design loosely-coupled data components
2. Scalability: Ensure architecture supports horizontal scaling
3. Observability: Add logs, metrics, data quality checks
4. Governance: Use Unity Catalog or equivalent for access and metadata
5. Lineage: Track where data comes from and how it's transformed
6. Security: Column-level encryption, tokenization, IAM

## Pipeline Architecture Example (Batch + Stream)
```
# Simulated: IoT Ingestion Layer
# Real-time ingestion using Spark Structured Streaming

from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, DoubleType

schema = StructType() \
    .add("device_id", StringType()) \
    .add("timestamp", StringType()) \
    .add("temperature", DoubleType()) \
    .add("humidity", DoubleType())

raw_stream = (spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "iot-events")
    .load())

parsed_stream = (raw_stream
    .selectExpr("CAST(value AS STRING)")
    .select(from_json(col("value"), schema).alias("data"))
    .select("data.*"))

# Write to bronze table (raw data)
(parsed_stream.writeStream
    .format("delta")
    .outputMode("append")
    .option("checkpointLocation", "/tmp/iot_chk")
    .start("/mnt/datalake/bronze/iot"))
```

## Data Governance and Lineage using Unity Catalog

```
-- Enable Unity Catalog table tracking
USE CATALOG main;

-- Example table
CREATE TABLE iot_bronze (
    device_id STRING,
    timestamp TIMESTAMP,
    temperature DOUBLE,
    humidity DOUBLE
)
COMMENT 'Raw sensor data from IoT devices';

-- Add tags for metadata management
ALTER TABLE iot_bronze SET TAGS ('source' = 'iot-sensors', 'sensitivity' = 'low');

-- Use system.access.audit or lineage views for governance
SELECT * FROM system.access.audit WHERE object_name = 'iot_bronze';
```
## Airflow DAG for Batch Layer Aggregation

```
# Aggregate IoT bronze data to silver layer using Airflow

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

dag = DAG('silver_aggregation', start_date=datetime(2023,1,1), schedule_interval='@hourly')

aggregate = BashOperator(
    task_id='aggregate_temp',
    bash_command='databricks jobs run-now --job-id 1234',
    dag=dag
)
```

## Staff Engineer Responsibilities in this context

1. Design reusable patterns: Define medallion architecture template across the org
2. Standarize pipeline templates: Airflow + Databricks notebooks with observability built-in
3. Cross-team platform enablement: Help analytic & ML teams onboard to catalog, CI/CD
4. Goverance enforment: Create policies for tagging, audit logs, data contracts
5. Mentor squads: Guide engineers in troubleshooting lineage issues or orchestration bugs
6. Review data SLAs: Set contracts between upstream and downstream teams
7. Producion support strategy: Establish runbooks, auto-healing jobs, escalation flows


