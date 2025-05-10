A retail platform wants to track incoming orders in real-time to update dashboards and alert logistics based on order volume and region.

1. Ingest Data Using Kafka + Autoloader (Simulated)

Simulate Kafka Source using Autoloader (S3 bucket as source)
```
df_orders = (spark.readStream
  .format("cloudFiles")
  .option("cloudFiles.format", "json")
  .option("cloudFiles.inferColumnTypes", "true")
  .load("/mnt/orders-stream/")
)

df_orders.writeStream \
  .format("delta") \
  .outputMode("append") \
  .option("checkpointLocation", "/mnt/checkpoints/orders/") \
  .start("/mnt/delta/orders/")
```

2. Add Watermark and Window Aggregation

```
from pyspark.sql.functions import *

df_with_time = df_orders \
  .withColumn("order_time", to_timestamp("order_time"))

windowed_df = df_with_time \
  .withWatermark("order_time", "10 minutes") \
  .groupBy(window("order_time", "5 minutes")) \
  .agg(count("*").alias("total_orders"))

windowed_df.writeStream \
  .format("delta") \
  .outputMode("complete") \
  .option("checkpointLocation", "/mnt/checkpoints/order_volume/") \
  .start("/mnt/delta/order_volume/")
```

3. Enable Change Data Feed (CDF)

```
ALTER TABLE delta./mnt/delta/orders/ SET TBLPROPERTIES (delta.enableChangeDataFeed = true);
```
Later, you can query changes like this:
```
SELECT * FROM table_changes('orders', '2024-05-01');
```

4. Query via Databricks SQL

```
-- Dashboard-ready table query
SELECT region, COUNT(*) as new_orders
FROM orders
WHERE order_time >= current_date()
GROUP BY region;
```

5. Monitoring + Optimization Tips

Use spark.databricks.delta.optimizeWrite.enabled = true for efficient small-file compaction.

Monitor stream latency via Databricks Structured Streaming UI.

Add alerts using SQL Alerts when orders spike beyond a threshold.
