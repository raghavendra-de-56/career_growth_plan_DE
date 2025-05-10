### 1. Kafka + Spark Structured Streaming

#### Q1. Read data from Kafka and count messages per topic in real-time.

Question: Write PySpark code to consume messages from Kafka and count how many messages are received per topic every 10 seconds.

Answer:
```
from pyspark.sql.functions import window

df = (
  spark.readStream
       .format("kafka")
       .option("kafka.bootstrap.servers", "localhost:9092")
       .option("subscribe", "orders")
       .load()
)

message_counts = (
  df.groupBy(window(df.timestamp, "10 seconds"))
    .count()
)

query = message_counts.writeStream \
                      .outputMode("complete") \
                      .format("console") \
                      .start()
```

#### 2. Schema Evolution with Delta Lake

Q2. Evolve schema dynamically in Delta Lake.

Question: Write PySpark code to append a new column payment_method into an existing Delta table with schema evolution.

Answer:
```
new_df = spark.read.json("new_data_with_payment.json")

new_df.write \
      .format("delta") \
      .option("mergeSchema", "true") \
      .mode("append") \
      .save("/mnt/delta/orders")
```

#### 3. Databricks SQL with Delta Tables

Q3. Query historical data using time travel.

Question: How would you query the data as it existed 3 versions ago in Databricks SQL?

Answer:
```
SELECT * FROM delta./mnt/delta/orders VERSION AS OF 3;
```

### 4. Detecting Late Data in Streaming

#### Q4. Write code to handle late data in Spark Structured Streaming using watermark.

Answer:
```
from pyspark.sql.functions import window

events = spark.readStream.format("kafka")...  # same as above

parsed = events.selectExpr("CAST(value AS STRING)", "timestamp")

agg = parsed.withWatermark("timestamp", "10 minutes") \
            .groupBy(window("timestamp", "5 minutes")) \
            .count()
```

### 5. Write Query to Z-Order a Delta Table

#### Q5. Optimize Delta table storage layout for querying user_id.

Answer:
```
OPTIMIZE delta./mnt/delta/orders ZORDER BY (user_id);
```
### 6. Implement a CDC pipeline using MERGE INTO

#### Q6. Merge incoming updates into a Delta table.

Answer:
```
deltaTable = DeltaTable.forPath(spark, "/mnt/delta/orders")

updatesDF = spark.read.format("json").load("s3://updates.json")

deltaTable.alias("target").merge(
    updatesDF.alias("source"),
    "target.order_id = source.order_id"
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
```
