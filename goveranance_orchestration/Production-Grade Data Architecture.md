## Production-Grade Data Architecture

### Here’s how everything fits together:

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
