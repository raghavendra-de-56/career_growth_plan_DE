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

### Real-World Example: IoT Sales Pipeline

Let’s simulate a business case of a smart retail system capturing IoT-based sales data.

#### 1. Bronze Layer (Raw Ingestion)
```
raw_iot_df = (
    spark.read.format("json")
    .load("/mnt/raw/iot_sales/")
)
# Save to bronze
raw_iot_df.write.format("delta").mode("overwrite").saveAsTable("bronze.iot_sales_raw")
```
Schema (raw):
```
{
  "device_id": "abc123",
  "timestamp": "2024-05-01T10:01:00Z",
  "product_id": 101,
  "price": 15.5,
  "store_id": "store_001",
  "customer_id": 1001
}
```

#### 2. Silver Layer (Dimensional Conforming)

We clean and enrich this data. Let’s join with dim_product and dim_customer.
```
bronze_df = spark.table("bronze.iot_sales_raw")

# Load dimensions
dim_product = spark.table("silver.dim_product")
dim_customer = spark.table("silver.dim_customer")

# Enrichment
silver_df = bronze_df.join(dim_product, "product_id") \
                     .join(dim_customer, "customer_id") \
                     .withColumn("sale_date", to_date("timestamp")) \
                     .select("device_id", "store_id", "product_id", "product_name", "category",
                             "customer_id", "customer_name", "region", "price", "sale_date")

# Save silver table
silver_df.write.format("delta").mode("overwrite").saveAsTable("silver.sales_enriched")
```
#### 3. Gold Layer (Fact Table)

We now aggregate this data into a Fact Table for BI use cases.
```
from pyspark.sql.functions import sum

gold_df = (
    silver_df.groupBy("sale_date", "store_id", "region", "category")
    .agg(sum("price").alias("daily_sales_amount"))
)

# Save gold fact table
gold_df.write.format("delta").mode("overwrite").saveAsTable("gold.fact_daily_sales")

```

### Visual Mapping to Star Schema

Fact Table (Gold): fact_daily_sales

Dimension Tables (Silver): dim_product, dim_customer, dim_store

```
                      +---------------------+
                       |   dim_customer      |
                       +---------------------+
                                 |
                                 |
                                 |
+---------------------+     +---------------------+     +-------------------+
|     dim_product     | --> |   fact_daily_sales  | <-- |     dim_store     |
+---------------------+     +---------------------+     +-------------------+
```
