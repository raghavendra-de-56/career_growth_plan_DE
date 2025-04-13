## Metadata Management

### What It Is:
Managing and tracking metadata (data about data): schema, usage, ownership, lineage, data quality, etc.

### Types of Metadata:
1. Technical: Schema, format, column names/types
2. Operational: Last updated, freshness, volume, errors
3. Business: Ownership, glossary terms, definitions
4. Social: Who uses it, how often, in which reports

### Key Tools:

1. Unity Catalog (auto metadata capture + APIs)
2. DataHub, Amundsen, OpenMetadata
3. dbt (docs + lineage + ownership metadata)

### Best Practices:

1. Automate metadata extraction (auto cataloging)
2. Embed metadata updates into CI/CD pipelines
3. Enable self-service search via metadata portals
4. Use metadata in pipeline logic (e.g., skip tables not updated in 7 days)

## Creating Metadata Schema for Tables
```
-- Create a table with rich metadata annotations
CREATE TABLE supply_chain.shipments (
  shipment_id STRING COMMENT 'Unique shipment identifier',
  order_id STRING COMMENT 'Associated order ID',
  carrier STRING COMMENT 'Shipping carrier',
  shipped_date DATE COMMENT 'Shipment date',
  delivery_status STRING COMMENT 'Delivered / In Transit / Returned'
)
COMMENT 'Shipment tracking table for logistics pipeline'
TBLPROPERTIES (
  'owner' = 'data_eng_team',
  'pii' = 'false',
  'retention' = '90_days'
);
```
## Querying and Refreshing Metadata
```
-- Query metadata
DESCRIBE EXTENDED supply_chain.shipments;

-- Refresh table metadata cache
MSCK REPAIR TABLE supply_chain.shipments;
```

## Tagging Columns and Tables with Unity Catalog

```
-- Tag a table with business context
ALTER TABLE supply_chain.shipments
SET TAGS ('classification' = 'internal', 'lifecycle' = 'operational');

-- Tag individual columns
ALTER TABLE supply_chain.shipments
ALTER COLUMN delivery_status
SET TAGS ('quality' = 'validated');
```

## Custom Metadata Tracking Using PySpark

```
from pyspark.sql.functions import lit, current_timestamp

df = spark.read.format("delta").table("supply_chain.shipments")

df = df.withColumn("ingestion_time", current_timestamp()) \
       .withColumn("source_system", lit("SAP_ECC")) \
       .withColumn("data_quality_score", lit("GOOD"))

df.write.format("delta").mode("overwrite").saveAsTable("curated.shipments_with_meta")
```
