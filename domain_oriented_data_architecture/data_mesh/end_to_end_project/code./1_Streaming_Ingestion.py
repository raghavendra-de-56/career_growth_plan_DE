# Notebook 2: Streaming Ingestion (Bronze Layer)

# Filename: 1.1_Streaming_Ingestion.ipynb

# Databricks Notebook - Streaming Ingestion

from pyspark.sql.functions import from_json, col

# Define schema for Kafka streaming data
stream_schema = StructType([
    StructField("order_id", StringType(), True),
    StructField("status", StringType(), True),
    StructField("update_time", TimestampType(), True),
])

# Read streaming data from Kafka
order_updates_stream = (spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "your-kafka-server:9092")
    .option("subscribe", "order-updates")
    .load())

# Parse JSON payload
order_updates_df = order_updates_stream.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), stream_schema).alias("data")) \
    .select("data.*")

# Write streaming data to Delta Bronze table
(order_updates_df.writeStream
    .format("delta")
    .option("checkpointLocation", "/mnt/datalake/checkpoints/bronze_streaming/")
    .outputMode("append")
    .start("/mnt/datalake/bronze/orders_streaming/"))
