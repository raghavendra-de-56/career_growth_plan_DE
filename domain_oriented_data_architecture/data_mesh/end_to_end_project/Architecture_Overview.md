## Architecture Overview

|Layer| Details|
|-----|--------|
|Source| Batch files from S3 + Kafka streaming for real-time order updates|
|Bronze Layer| Raw ingestion(as-is dump into Delta tables|
|Silver Layer| Apply data quality checks(nulls, duplicates, outliers)|
|Gold Layer| Clean modeled dta for business use (order fact table | customer dimension)|
|Orchestration| Airflow DAG to manage ingestion and quality checks|
|Monitoring|Databricks dashboards for SLA monitoring|

