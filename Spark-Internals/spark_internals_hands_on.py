# Databricks Notebook: Spark Internals Hands-on Exercises

# 1️⃣ Understanding DAG & Execution Plan
df = spark.range(1, 1000000)  # Create a DataFrame with 1M rows
df = df.withColumnRenamed("id", "value")
df_filtered = df.filter(df["value"] % 2 == 0)  # Filter even numbers
df_filtered.explain(True)  # Show Execution Plan
df_filtered.count()  # Action triggers execution

# Real-World Scenario: Processing Web Server Logs
df_logs = spark.read.json("/databricks-datasets/iot-stream/data.json")
df_logs_filtered = df_logs.filter(df_logs["temperature"] > 50)
df_logs_filtered.explain(True)
df_logs_filtered.show()

# Advanced Scenario: Real-time Streaming Pipeline for IoT Data
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark.sql.functions import from_json

schema = StructType([
    StructField("device_id", StringType(), True),
    StructField("temperature", IntegerType(), True),
    StructField("humidity", IntegerType(), True)
])

df_stream = (spark
    .readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "iot_topic")
    .load()
    .selectExpr("CAST(value AS STRING) as json")
    .select(from_json("json", schema).alias("data"))
    .select("data.*"))

df_stream.writeStream.format("console").start()

# 2️⃣ Catalyst Optimizer & Predicate Pushdown
df = spark.read.parquet("/databricks-datasets/nyctaxi/tripdata/parquet/")
df_filtered = df.filter(df["passenger_count"] > 2)
df_filtered.explain(True)  # Check predicate pushdown
df_filtered.show()

# Advanced Scenario: Query Performance Optimization in Data Lakes
df_large = spark.read.parquet("s3://enterprise-data-lake/transactions/")
df_filtered = df_large.filter("transaction_amount > 1000 AND region = 'US'")
df_filtered.explain(True)
df_filtered.show()

# 3️⃣ Shuffle Optimization with Broadcast Joins
from pyspark.sql.functions import broadcast
df_large = spark.range(1, 100000000).withColumnRenamed("id", "large_id")
df_small = spark.range(1, 1000).withColumnRenamed("id", "small_id")

# Without Broadcast
df_joined = df_large.join(df_small, df_large.large_id == df_small.small_id)
df_joined.explain(True)

# With Broadcast
df_broadcasted = df_large.join(broadcast(df_small), df_large.large_id == df_small.small_id)
df_broadcasted.explain(True)

# Advanced Scenario: Optimizing Large-Scale Customer Segmentation Joins
df_customer_profiles = spark.read.parquet("s3://data-lake/customers/")
df_purchases = spark.read.parquet("s3://data-lake/purchases/")

df_joined = df_purchases.join(broadcast(df_customer_profiles), "customer_id")
df_joined.explain(True)
df_joined.show()

# 4️⃣ Partitioning for Performance Optimization
df = spark.range(1, 1000000).withColumnRenamed("id", "value")
print(df.rdd.getNumPartitions())

# Increase Partitions
df_repartitioned = df.repartition(10)
print(df_repartitioned.rdd.getNumPartitions())

df.write.partitionBy("value").parquet("/tmp/partitioned_data")

# Advanced Scenario: Data Skew Handling with Salting
df_skewed = spark.read.parquet("/databricks-datasets/retail-org/orders")
df_skewed = df_skewed.withColumn("salt", (df_skewed["customer_id"] % 10))
df_partitioned = df_skewed.repartition("salt")
df_partitioned.write.partitionBy("salt").parquet("/tmp/skewed_partitioned")

# 5️⃣ Tungsten Engine & Memory Optimization
from pyspark.storagelevel import StorageLevel
df = spark.range(1, 50000000).withColumnRenamed("id", "value")

df_cached = df.cache()
df_cached.count()

df_persisted = df.persist(StorageLevel.MEMORY_AND_DISK)
df_persisted.count()

# Advanced Scenario: Memory-Efficient Large Dataset Aggregations
df_large_data = spark.read.parquet("s3://enterprise-data-lake/sales_data/")
df_large_data = df_large_data.repartition(50)
df_aggregated = df_large_data.groupBy("region").sum("sales_amount")
df_aggregated.persist(StorageLevel.DISK_ONLY)
df_aggregated.show()

# 6️⃣ File Formats & Read Performance
import time
df = spark.range(1, 1000000).withColumnRenamed("id", "value")

df.write.mode("overwrite").csv("/tmp/data_csv")
df.write.mode("overwrite").parquet("/tmp/data_parquet")

# Read CSV & Measure Time
start_time = time.time()
df_csv = spark.read.csv("/tmp/data_csv", inferSchema=True, header=True)
df_csv.count()
print("CSV Read Time:", time.time() - start_time)

# Read Parquet & Measure Time
start_time = time.time()
df_parquet = spark.read.parquet("/tmp/data_parquet")
df_parquet.count()
print("Parquet Read Time:", time.time() - start_time)

# Advanced Scenario: Optimizing Read Performance for Incremental Data Processing
df_incremental = spark.read.parquet("s3://enterprise-data-lake/orders/2025-03-31/")
df_incremental.createOrReplaceTempView("new_orders")

# Using Delta Lake for Incremental Processing
from delta.tables import DeltaTable

delta_table = DeltaTable.forPath(spark, "s3://enterprise-data-lake/orders_delta")
delta_table.alias("old").merge(
    df_incremental.alias("new"), "old.order_id = new.order_id"
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
