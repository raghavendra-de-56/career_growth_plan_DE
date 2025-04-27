# Notebook 3: Data Quality Checks (Silver Layer)

# Filename: 2.0_Data_Quality_Checks.ipynb

# Databricks Notebook - Data Quality

# Load raw bronze orders
bronze_orders_df = spark.read.format("delta").load("/mnt/datalake/bronze/orders_batch/")

# Simple data validations
valid_orders_df = bronze_orders_df.filter(
    (bronze_orders_df.order_amount > 0) &
    (bronze_orders_df.customer_id.isNotNull())
)

# Write valid data to Silver
valid_orders_df.write.format("delta") \
    .mode("overwrite") \
    .save("/mnt/datalake/silver/orders/")
