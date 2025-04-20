### Data Quality Checks with Great Expectations + Delta Lake

Scenario: You're validating incoming sales data from a Bronze → Silver pipeline in Databricks.
```
# Install Great Expectations (only if not already available in cluster)
# %pip install great_expectations

# Step 1: Create sample raw (bronze) sales data
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from datetime import datetime

spark = SparkSession.builder.appName("Week5-DataQuality").getOrCreate()

raw_data = [
    (1, "2023-04-01", 100.5, "USD"),
    (2, "2023-04-02", 200.0, "USD"),
    (3, "2023-04-02", None, None),  # Invalid row
]

columns = ["order_id", "order_date", "amount", "currency"]

df_raw = spark.createDataFrame(raw_data, columns)
df_raw.write.mode("overwrite").format("delta").save("/tmp/bronze/sales")

# Step 2: Run simple data validation manually using expectations

from great_expectations.dataset import SparkDFDataset

ge_df = SparkDFDataset(df_raw)

# Expect no nulls in order_id
assert ge_df.expect_column_values_to_not_be_null("order_id")["success"]

# Expect amount to be >= 0
print(ge_df.expect_column_values_to_be_between("amount", 0, None))

# Expect currency to be one of valid codes
print(ge_df.expect_column_values_to_be_in_set("currency", ["USD", "EUR"]))

# Step 3: Filter out bad data and write to Silver

df_valid = df_raw.filter(col("amount").isNotNull() & col("currency").isNotNull())
df_valid.write.mode("overwrite").format("delta").save("/tmp/silver/sales")

# Step 4: Record quality check metrics for observability

from pyspark.sql.functions import lit, current_timestamp

total_records = df_raw.count()
valid_records = df_valid.count()

metrics_df = spark.createDataFrame([
    ("sales", current_timestamp(), total_records, valid_records, valid_records / total_records)
], ["table_name", "run_time", "total_records", "valid_records", "success_ratio"])

metrics_df.write.mode("append").format("delta").save("/tmp/metrics/data_quality")

# View metrics for SLA reporting
display(spark.read.format("delta").load("/tmp/metrics/data_quality"))

```
