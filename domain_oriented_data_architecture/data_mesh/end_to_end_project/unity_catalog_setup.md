Unity Catalog Setup for Our Retail Order Processing Project

Unity Catalog in Databricks provides centralized metadata management, access control, and full lineage tracking across all tables, views, files, and pipelines.

We’ll organize it this way:

### Unity Catalog Organization

|Level|Name|Purpose|
|-----|-----|------|
|Metastore| retail_metastore|Central place to manage all data assests|
|Catalog|retail_catalog|Separate retail project assests from others|
|Schema|bronze, silver, gold|Reflect medallion architcture inside catalog|
|Tables| orders_batch, orders_streaming, fact_sales, dim_customer_orders| Data assets in each layer|

### Create Metastore (Admin Task)

(Usually set up once per workspace.)
```
# No code - Admin Console - Unity Catalog Setup
# Create a Metastore named retail_metastore
# Assign it to your Databricks workspace

```

### Create Catalog and Schemas

(Execute as Databricks SQL commands in a Notebook)
```
-- Create Catalog
CREATE CATALOG IF NOT EXISTS retail_catalog 
MANAGED LOCATION 's3://your-unity-catalog-path/retail_catalog/';

USE CATALOG retail_catalog;

-- Create Schemas
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
```
### Register Tables in Unity Catalog

When saving your tables, save inside Unity Catalog schema instead of DBFS folder.

Example changes:

Instead of:
```
.save("/mnt/datalake/bronze/orders_batch/")
```
Change to:
```
.saveAsTable("retail_catalog.bronze.orders_batch")
```
Same for Silver and Gold layers!

### Unity Catalog Lineage Visualization

Go to Databricks UI → Data → Lineage tab

You will see automatic lineage:

Example:

S3 Orders CSV → Bronze.orders_batch → Silver.orders_validated → Gold.fact_sales

Track transformations from raw ingestion to business facts!

### Access Control (Fine Grained)

You can assign table-level, column-level, and row-level permissions easily.

Example:
```
GRANT SELECT ON TABLE retail_catalog.gold.fact_sales TO finance_analysts_group;

GRANT SELECT (customer_id, total_sales) ON TABLE retail_catalog.gold.fact_sales TO auditors_group;
```
This ensures only authorized users can view sensitive customer or sales data.

### Summary: Unity Catalog Setup

|Feature| Benefit|
|-------|--------|
|Centralized Metastore| One place to track all assests|
|Fine-grained Access|Secure Sensitive data|
|Full Leneage| End-to-end visibility|
|Compliance| Easy GDPR/CCPA compilance|
|Schema Enforcement| No accidental schema drift|


### Quick Visual Overview
```
S3 -> Bronze.orders_batch --> Silver.orders_validated --> Gold.fact_sales
    (Batch CSV)       (Cleaned)                   (Aggregated)
    
    +
Kafka -> Bronze.orders_streaming --> Silver.orders_updates
    (Streaming)              (Validated status updates)
    
    +
Monitoring with Databricks SQL
Lineage with Unity Catalog
```


