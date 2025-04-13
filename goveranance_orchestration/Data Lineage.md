## Data Lineage

### What It Is:
Tracking the full journey of data from source to consumption — showing how it's transformed, joined, filtered, and visualized.

### Why It Matters:

1. Impact analysis before schema changes
2. Debugging data quality issues
3. Regulatory audits and compliance
4. Building trust with stakeholders

### Tools:

1. Unity Catalog (native UI for table/column lineage)
2. DataHub, OpenMetadata, Atlan, Collibra
3. dbt lineage graphs

### Use Case:

```
iot_raw.temperature  -->  validated.temperature
                           |
                           --> enriched.temp_celsius
                                   |
                                   --> powerbi_iot_dashboard
```

### Implementation Tips:

1. Use tools with automated lineage capture (Unity Catalog, dbt)
2. Complement with manual annotations for critical flows
3. Version control DAGs and transformations
4. Track schema changes and propagate downstream alerts

## What Is Data Lineage?

Data Lineage refers to the journey of data from its source to final destination—across pipelines, transformations, and consumption layers. It answers questions like:

1. Where did this data come from?
2. How was it transformed?
3. What downstream systems rely on it?
4. Who accessed or modified it?

## Why It Matters

1. Design lineage-aware architecture
2. Ensure traceability and auditability
3. Debug pipeline failures quickly
4. Assess impact of schema changes
5. Enable governance, compliance & observability

## Lineage Architecture Overview (Databricks + Unity Catalog)
```
┌──────────────────────┐
│   Source Systems     │  (RDS, APIs, Kafka)
└────────┬─────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│ Ingestion Layer (Spark / Autoloader / Airflow)               │
│   - Track source + ingestion logic                           │
└────────┬─────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│ Processing Layer (Delta Live Tables / PySpark / dbt)         │
│   - Lineage metadata auto-tracked in Unity Catalog           │
│   - Fine-grained tracking at table + column level            │
└────────┬─────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│ Curated Zone (Delta Lake)                                    │
│   - Data tagged, secured, and versioned                      │
└────────┬─────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│ BI & ML Consumers (PowerBI, Tableau, Feature Store, MLflow)  │
│   - Downstream dependencies tracked                          │
└──────────────────────────────────────────────────────────────┘

```

## Lineage Example with Databricks Unity Catalog

Unity Catalog automatically tracks end-to-end lineage across notebooks, workflows, jobs, Delta Live Tables, and SQL queries.

### Enable Lineage (No code required)

Databricks auto-captures lineage when using:
1. SQL editor
2. Notebooks
3. Workflows (Jobs)
4. Delta Live Tables (DLT)

### Just query and transform using standard commands:
```
CREATE TABLE curated.forecast_data AS
SELECT
  o.product_id,
  o.country,
  f.forecast_units,
  CURRENT_DATE() AS snapshot_date
FROM raw.orders AS o
JOIN raw.forecasts AS f
  ON o.product_id = f.product_id;
```
Unity Catalog lineage view will show:

Upstream: raw.orders, raw.forecasts

Downstream: curated.forecast_data

### Query Lineage Programmatically (Preview)

You can fetch lineage using Databricks REST API (for now only available in Unity Catalog-enabled workspaces).

Example endpoint:
```
GET /api/2.0/unity-catalog/lineage/table/<catalog.schema.table>
```

### Custom Lineage Tracking in PySpark

For custom Spark jobs outside DLT or Unity Catalog, implement manual lineage tagging.
```
from pyspark.sql import SparkSession
from datetime import datetime

spark = SparkSession.builder.getOrCreate()

df_orders = spark.read.format("delta").table("raw.orders")
df_forecast = spark.read.format("delta").table("raw.forecasts")

df_joined = df_orders.join(df_forecast, "product_id")

# Add lineage metadata
df_joined = df_joined.withColumn("lineage_source", lit("orders, forecasts"))
df_joined = df_joined.withColumn("lineage_job", lit("forecast_model_etl"))
df_joined = df_joined.withColumn("lineage_timestamp", lit(datetime.now().isoformat()))

df_joined.write.format("delta").mode("overwrite").saveAsTable("curated.forecast_data")
```

### dbt + Unity Catalog Integration for Lineage

If you're using dbt in Databricks, it auto-generates lineage through the dbt DAG:
```
-- models/curated_forecast.sql
SELECT
  o.product_id,
  f.forecast_units
FROM {{ ref('orders') }} o
JOIN {{ ref('forecasts') }} f
  ON o.product_id = f.product_id
```
This gets captured in dbt docs + Unity Catalog Lineage view.

## Real-World Use Case

### Scenario:

You own a supply chain product that integrates order, inventory, and forecast data.

A report showing mismatched quantities was flagged.

### How Lineage Helps:

1. Use Unity Catalog lineage view to trace forecast_report back to inventory_snapshots and orders_raw.
2. Identify transformation step with a filter bug.
3. Fix logic, reprocess downstream tables only if impacted (impact analysis).

## Interview-Grade Talking Points

1. “Can you explain how you implemented data lineage?”

Describe your use of Unity Catalog auto-lineage and custom tracking in Spark jobs.

Explain usage of audit tables or metadata tagging.

2. “How do you debug data quality issues?”

Use lineage to trace input sources, transformations, affected downstream tables.

Demonstrate understanding of backward and forward impact analysis.

3. “What’s the difference between technical vs business lineage?”

Technical: column-level and process-level traceability

Business: logical flow from business terms (e.g., customer orders) to metrics

## Summary Checklist
Area: Mist-Haves

Auto Lineage: Unit Catalog DLT, dbt

Manual Lineage: Spark job tagging, metadata columns

Impact Analysis Tools: Unit Catalog Lineage UI, DataHub, OpenLineage

Documentation: Linok lineage to Confluence / Data Catalog

Access Logs + Auditing: Track data usage and lineage through audit logs.
