### Medallion Architecture
The Medallion Architecture is a best-practice framework widely used in Lakehouse platforms like Databricks to build scalable, modular, and efficient data pipelines. It aligns perfectly with dimensional modeling concepts, like fact and dimension tables, and supports real-time + batch use cases.

Let’s dive deep — with theory + practical PySpark/Delta examples.

### Overview

The architecture is structured into three layers:

Bronze: Raw ingestion layer. Example: Raw IoT, logs, JSON, CSV, API responses

Silver: Cleaned, enriched data (joins, filters). Example: Flattened tables, dimension tables

Gold: Business-level aggregates, marts, facts. Example: KPIs, metric, dashboards, fact tables

# Mapping Medallion Layers to Dimensional Modeling

| Data Model Component | Layer | Description |
|:-------------------: |:------:|:----------:|
|Raw dimension & fact data | Bronze | No modeling, just ingested data |
|Confirmed Dimensions | Silver | Cleaned dimensions (e.g. dim_customer) |
|Star Schema Fact Tables | Gold | Fact_sales, Fact_inventory|
|Aggregates. KPIs | Gold | Revenue by region, Avg order size|

