# Streaming Data Ingestion (Kafka Stream)

# Real-time order updates (new fields like payment_mode etc.).

# Handle schema evolution dynamically!

# Kafka stream ingestion
orders_stream = (
  spark.readStream
       .format("kafka")
       .option("kafka.bootstrap.servers", "broker:9092")
       .option("subscribe", "orders_topic")
       .load()
)

# Parse JSON payload
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

schema = StructType([
    StructField("order_id", StringType()),
    StructField("order_date", StringType()),
    StructField("customer_id", StringType()),
    StructField("order_total", DoubleType()),
    StructField("payment_mode", StringType()),  # Schema evolution field
])

orders_stream_parsed = orders_stream.selectExpr("CAST(value AS STRING)").select(from_json(col("value"), schema).alias("data")).select("data.*")

orders_stream_parsed.writeStream \
    .format("delta") \
    .option("checkpointLocation", "/mnt/delta/orders_stream/_checkpoint") \
    .outputMode("append") \
    .table("bronze.orders_stream")
