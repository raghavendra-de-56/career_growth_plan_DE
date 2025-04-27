# Data Quality Validation (Silver Layer)

# Null check, duplicate check, outlier detection.

# Generate alerts if data fails.

# Merge batch + streaming
orders_combined = spark.sql("""
SELECT * FROM bronze.orders_raw
UNION ALL
SELECT * FROM bronze.orders_stream
""")

# Data quality checks
critical_columns = ["order_id", "order_date", "customer_id", "order_total"]
for col_name in critical_columns:
    null_count = orders_combined.filter(col(col_name).isNull()).count()
    if null_count > 0:
        raise Exception(f"Nulls found in column: {col_name}")

# No issues: move to silver
orders_combined.write.format("delta").mode("overwrite").saveAsTable("silver.orders_cleaned")

