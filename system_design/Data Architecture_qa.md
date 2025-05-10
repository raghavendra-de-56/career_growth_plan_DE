###  Data Architecture Questions

#### Q1. How do you implement data quality SLAs in real-time pipelines?

Define SLAs: e.g., 99.9% of messages processed in under 1 minute

Implement SLIs/SLOs: % messages processed in SLA window

Use tools like Great Expectations, Databricks Quality Expectations, Delta Live Tables (DLT)

Example:
```
from great_expectations.dataset import SparkDFDataset

df_ge = SparkDFDataset(parsed_df)
df_ge.expect_column_values_to_not_be_null("device_id")
```

#### Q2. How do you ensure data lineage in real-time pipelines?

Use Unity Catalog to track table/table lineage.

Use Delta Live Tables (DLT): built-in lineage tracking.

Maintain audit columns: source, event_time, ingestion_time.

### Coding Interview Questions & Solutions

#### Q1. How do you handle out-of-order and late events in streaming data?

Spark Example using Watermarking:
```
parsed_df.withWatermark("event_time", "10 minutes") \
    .groupBy("device_id", window("event_time", "5 minutes")) \
    .agg(avg("temperature").alias("avg_temp"))
```

#### Q2. Write a PySpark job to deduplicate records using Delta Lake.

```
from delta.tables import DeltaTable

deltaTable = DeltaTable.forPath(spark, "/mnt/delta/silver")
deduplicated = (deltaTable.toDF()
                .withColumn("rn", row_number().over(Window.partitionBy("id").orderBy(desc("timestamp"))))
                .filter("rn = 1"))

deduplicated.write.format("delta").mode("overwrite").save("/mnt/delta/gold")
```
