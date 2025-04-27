## SLA (Agreement)
1. Description: Contract between teams on expectations
2. Example: Data must arrive by 8 AM daily

## SLO (Objective)
1. Description: Internal goal that drives reliability
2. Example: 99% of daily jobs complete in 5 min

## SLI (Indicator)
1. Description: Metric to track the objective
2. Example: Job latency, data accuracy %
   




### SLA/SLI/SLO Monitoring in Databricks Workflows

Goal: Build a simple framework to measure data freshness and SLA compliance for a Silver table (e.g., sales), and publish SLI/SLO metrics to a Delta-based monitoring table.

```
# Step 1: Define your SLA & SLO

# SLA: Sales data should be updated daily by 8 AM
# SLO: 99% of runs per month should meet this SLA

# Step 2: Simulate daily update to Silver table

from pyspark.sql.functions import current_timestamp
from datetime import datetime

# Simulate a batch update to Silver table
df = spark.read.format("delta").load("/tmp/silver/sales")
df = df.withColumn("last_updated", current_timestamp())
df.write.mode("overwrite").format("delta").save("/tmp/silver/sales")

# Step 3: Write a job that checks freshness (SLI)

from pyspark.sql.functions import col, unix_timestamp, lit
from datetime import datetime, timedelta

now = datetime.now()
sla_time = datetime(now.year, now.month, now.day, 8, 0, 0)  # Today 8 AM

df_latest = spark.read.format("delta").load("/tmp/silver/sales")
max_update_time = df_latest.selectExpr("max(last_updated) as max_time").first()["max_time"]

# Calculate freshness metric
freshness_seconds = (now - max_update_time).total_seconds()
sla_met = max_update_time <= sla_time

print(f"Max Update Time: {max_update_time}")
print(f"SLA Time: {sla_time}")
print("SLA Met:", sla_met)

# Step 4: Log SLI/SLO data into monitoring table

sli_df = spark.createDataFrame([(
    "sales_silver", now, max_update_time, sla_time, sla_met
)], ["table_name", "check_time", "last_updated", "sla_time", "sla_met"])

sli_df.write.mode("append").format("delta").save("/tmp/metrics/sli_monitoring")

# Step 5: Analyze SLA breach % over time

metrics_df = spark.read.format("delta").load("/tmp/metrics/sli_monitoring")
metrics_df.createOrReplaceTempView("sli_monitoring")

spark.sql("""
SELECT
  table_name,
  COUNT(*) as total_checks,
  SUM(CASE WHEN sla_met THEN 1 ELSE 0 END) as sla_passed,
  ROUND(100.0 * SUM(CASE WHEN sla_met THEN 1 ELSE 0 END)/COUNT(*), 2) as sla_success_rate
FROM sli_monitoring
GROUP BY table_name
""").show()
```


Key Concepts Covered:

Defining SLAs (e.g., freshness deadlines)

Measuring SLIs (actual freshness)

Calculating SLO metrics (success rate)

Writing results into monitoring tables (for dashboards or alerts)
