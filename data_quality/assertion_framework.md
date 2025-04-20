### Data Quality Assertion Framework with PySpark (Databricks)

Goal: Build a lightweight, modular data quality framework that can validate source/ingested data against a set of assertions before moving to Silver or Gold layers.

Step 1: Sample Raw Data
```
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

data = [
    ("101", "Nike", 100.0),
    ("102", "Adidas", 200.5),
    (None, "Puma", 150.0),          # Missing ID
    ("104", "", 130.0),             # Blank brand
    ("105", "Reebok", -10.0),       # Invalid price
]

df = spark.createDataFrame(data, ["id", "brand", "price"])
df.show()
```
Step 2: Define Data Quality Rules
```
# Simple rules defined as a list of lambdas
rules = [
    ("Not Null - id", lambda df: df.filter(col("id").isNull()).count() == 0),
    ("Brand Not Blank", lambda df: df.filter((col("brand") == "") | col("brand").isNull()).count() == 0),
    ("Price Positive", lambda df: df.filter(col("price") < 0).count() == 0)
]
```
Step 3: Apply Assertions and Collect Results
```
from datetime import datetime

results = []
for rule_name, rule_fn in rules:
    try:
        status = "PASS" if rule_fn(df) else "FAIL"
    except Exception as e:
        status = "ERROR"
    results.append((datetime.now(), rule_name, status))

# Convert results to a Spark DataFrame
dq_results_df = spark.createDataFrame(results, ["check_time", "rule_name", "status"])
dq_results_df.show()
```

Step 4: Store Results in Delta for Monitoring
```
dq_results_df.write.mode("append").format("delta").save("/tmp/monitoring/dq_checks")
```

Optional Step: Stop Pipeline if Rules Fail
```
if "FAIL" in [r[2] for r in results]:
    raise Exception("Data Quality Check Failed. Aborting pipeline.")
```

### Enhancements for Production:
1. Use Great Expectations or Deequ if you want formal test suites.
2. Integrate with Databricks Workflows for automated checks.
3. Store baseline metrics and create SLIs/SLOs for DQ performance.
