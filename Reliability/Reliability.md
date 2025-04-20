### Data Pipeline Reliability Patterns (Retries, Alerts, Failures)

Goal: Simulate failure handling and retry patterns for a data ingestion pipeline. This is especially critical for resilient, production-grade pipelines.


Step 1: Define a Simulated Unreliable Source
```
# Simulate a flaky data source: 50% chance of failure
import random
from pyspark.sql.utils import AnalysisException

def unreliable_read():
    if random.random() > 0.5:
        raise Exception("Data source failed!")
    else:
        return spark.createDataFrame([
            ("001", "Nike"), 
            ("002", "Adidas")
        ], ["id", "brand"])

try:
    df = unreliable_read()
    df.show()
except Exception as e:
    print("Initial Load Failed:", e)
```
Step 2: Add a Retry Wrapper
```
import time

def retry(func, retries=3, delay=5):
    for attempt in range(1, retries + 1):
        try:
            print(f"Attempt {attempt}")
            return func()
        except Exception as e:
            print(f"Retry {attempt} failed: {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                raise Exception("All retries failed")

# Usage
try:
    df_reliable = retry(unreliable_read, retries=3, delay=2)
    df_reliable.write.mode("overwrite").format("delta").save("/tmp/silver/brands")
except Exception as final_err:
    print("Pipeline failed after retries. Trigger alert or circuit breaker.")
```
Step 3: Capture Failure Logs
```
from datetime import datetime

failure_log_df = spark.createDataFrame([
    ("brand_pipeline", datetime.now(), str(final_err), "FAILED")
], ["pipeline_name", "failure_time", "error", "status"])

failure_log_df.write.mode("append").format("delta").save("/tmp/monitoring/pipeline_failures")
```

Step 4: Alert via Logging or Email (Optional Integration)

In production, this log table can be integrated with:

Slack alerts

PagerDuty triggers

Databricks SQL Dashboard for visualization


### Concepts Covered:

1. Retry strategy for unstable data sources
2. Logging pipeline status
3. Fault-tolerant design with observability
4. Proactive failure management patterns
