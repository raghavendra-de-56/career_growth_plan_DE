### End-to-End Pipeline Reliability with SLO Enforcement and Alerting

Objective: Simulate an end-to-end streaming pipeline with:

SLA/SLO monitoring

Logging & alerting

Circuit breaker pattern on quality or latency failure

#### Step 1: Simulate a Streaming Source
```
from pyspark.sql.types import StructType, StringType, DoubleType
from pyspark.sql.functions import current_timestamp

schema = StructType() \
    .add("id", StringType()) \
    .add("brand", StringType()) \
    .add("price", DoubleType())

stream_df = (spark.readStream
             .schema(schema)
             .option("maxFilesPerTrigger", 1)
             .json("/databricks-datasets/retail-org/customers"))

stream_df = stream_df.withColumn("ingestion_time", current_timestamp())
```

#### Step 2: Simulate a Data Quality Assertion in Streaming
```
from pyspark.sql.functions import col

def validate_stream(df):
    return df.filter(col("price").isNotNull() & (col("price") > 0))

validated_df = validate_stream(stream_df)

```

#### Step 3: Monitor for SLA/SLO Violation

Simulate writing to a Bronze table and measuring processing latency:
```
from pyspark.sql.functions import expr

output_df = validated_df \
    .withColumn("processing_time", current_timestamp()) \
    .withColumn("latency_sec", expr("unix_timestamp(processing_time) - unix_timestamp(ingestion_time)"))

query = (output_df.writeStream
         .outputMode("append")
         .format("delta")
         .option("checkpointLocation", "/tmp/checkpoints/bronze_pipeline")
         .start("/tmp/bronze/iot_stream"))
```

#### Step 4: Create a Monitoring Table for SLOs
```
# In real case, aggregate latency and compare with SLO threshold
latency_df = output_df.select("id", "latency_sec")
(latency_df.writeStream
    .outputMode("append")
    .format("delta")
    .option("checkpointLocation", "/tmp/checkpoints/slo_monitoring")
    .start("/tmp/monitoring/latency"))
```

#### Step 5: Alerting Logic (Simulated)

You can periodically run this as a batch job:
```
df = spark.read.format("delta").load("/tmp/monitoring/latency")
if df.filter("latency_sec > 5").count() > 10:
    print("ALERT: SLA breached on latency for >10 records.")
    # Trigger webhook / email / Slack integration here
```

#### Step 6: Stop or Reroute Pipeline on Persistent Failures

If SLOs consistently fail:

Reroute stream to quarantine table

Send alert to stop pipeline

Notify engineering or product teams


### What You Built Here:

Streaming pipeline from raw source

Real-time DQ check

Latency monitoring (SLO)

Alert triggering logic

Circuit-breaker-style flow to stop pipeline
