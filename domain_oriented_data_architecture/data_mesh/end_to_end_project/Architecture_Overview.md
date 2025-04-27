## Architecture Overview

|Layer| Details|
|-----|--------|
|Source| Batch files from S3 + Kafka streaming for real-time order updates|
|Bronze Layer| Raw ingestion(as-is dump into Delta tables|
|Silver Layer| Apply data quality checks(nulls, duplicates, outliers)|
|Gold Layer| Clean modeled dta for business use (order fact table | customer dimension)|
|Orchestration| Airflow DAG to manage ingestion and quality checks|
|Monitoring|Databricks dashboards for SLA monitoring|


## Summary Diagram
```
[S3 Orders] --> [Bronze Layer (raw ingest)] --> [Silver Layer (data validated)] --> [Gold Layer (business model)]
      +                                                      +
    [Kafka]                                            [Data Quality Failures]
                                                         |
                                                      [Alerts via Slack]
                                                         |
                                                      [Lineage tracked in Unity Catalog]

```
