# Notebook Code: Data Quality Validator

# Databricks notebook: data_quality_framework

from pyspark.sql.functions import col, count, when, isnan

# Load raw data
df = spark.read.format("delta").load("/mnt/retail/orders/raw")

# Define critical columns to check
critical_columns = ["order_id", "order_date", "customer_id", "order_total"]

# 1. Null Check
null_checks = df.select([
    (count(when(col(c).isNull() | isnan(c), c)) / count("*")).alias(f"{c}_null_percentage") for c in critical_columns
])

null_checks.show()

# 2. Duplicate Check
duplicate_count = df.groupBy(critical_columns).count().filter(col("count") > 1).count()

print(f"Duplicate Rows: {duplicate_count}")

# 3. Outlier Detection (Order total > 1 million considered outlier)
outliers = df.filter(col("order_total") > 1_000_000)
outlier_count = outliers.count()

print(f"Outlier Rows (Order total > 1M): {outlier_count}")

# 4. Schema Validation
expected_fields = set(["order_id", "order_date", "customer_id", "order_total"])
actual_fields = set(df.columns)

missing_fields = expected_fields - actual_fields
new_fields = actual_fields - expected_fields

print(f"Missing fields: {missing_fields}")
print(f"New fields: {new_fields}")

# Final Status
if duplicate_count == 0 and outlier_count == 0 and not missing_fields:
    print("Data quality passed")
else:
    print("Data quality issues detected! Investigate!")
