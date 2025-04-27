# Notebook 1: Batch Ingestion (Bronze Layer)

# Filename: 1.0_Batch_Ingestion.ipynb

# Databricks Notebook - Batch Ingestion

from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType

# Define schema
order_schema = StructType([
    StructField("order_id", StringType(), True),
    StructField("customer_id", StringType(), True),
    StructField("order_amount", IntegerType(), True),
    StructField("order_date", TimestampType(), True),
])

# Read batch orders from S3
batch_orders_df = spark.read \
    .schema(order_schema) \
    .option("header", "true") \
    .csv("s3://retail-data/orders_batch/")

# Write to Delta Bronze table
batch_orders_df.write.format("delta") \
    .mode("append") \
    .save("/mnt/datalake/bronze/orders_batch/")
