Databricks notebook source

Week 2 - Real World Project: Retail Order Processing Pipeline

COMMAND ----------

Step 1: Simulate Ingestion - Orders and Customers

from pyspark.sql.functions import * from pyspark.sql.types import * import random

Simulate Orders DataFrame

order_schema = StructType([ StructField("order_id", StringType()), StructField("customer_id", StringType()), StructField("order_date", DateType()), StructField("amount", DoubleType()) ])

order_data = [ (f"ORD{i}", random.choice(["C001", "C002", "C003", "C004", "C005", "C_SKEWED"]), datetime.date(2024, 1, random.randint(1, 28)), round(random.uniform(100, 500), 2)) for i in range(1, 5001) ]

orders_df = spark.createDataFrame(order_data, schema=order_schema) orders_df.write.format("delta").mode("overwrite").save("/mnt/delta/retail/orders")

Simulate Customers DataFrame

customer_data = [("C001", "Alice"), ("C002", "Bob"), ("C003", "Charlie"), ("C004", "David"), ("C005", "Eve"), ("C_SKEWED", "BigCustomer")] customer_df = spark.createDataFrame(customer_data, ["customer_id", "name"]) customer_df.write.format("delta").mode("overwrite").save("/mnt/delta/retail/customers")

COMMAND ----------

Step 2: Handle Skew Using Salting

orders_skewed = spark.read.format("delta").load("/mnt/delta/retail/orders") orders_skewed = orders_skewed.withColumn("salt", (rand() * 10).cast("int")) orders_skewed = orders_skewed.withColumn("salted_key", concat_ws("_", "customer_id", col("salt")))

Expand customer data for join

customer_df = spark.read.format("delta").load("/mnt/delta/retail/customers") customers_salted = customer_df.crossJoin(spark.range(0, 10).withColumnRenamed("id", "salt")) customers_salted = customers_salted.withColumn("salted_key", concat_ws("_", "customer_id", col("salt")))

Join using salted keys

joined_df = orders_skewed.join(customers_salted, "salted_key").drop("salt", "salted_key") joined_df.write.format("delta").mode("overwrite").save("/mnt/delta/retail/joined_orders")

COMMAND ----------

Step 3: Merge Daily Order Updates

from delta.tables import *

Simulate update for a few orders

order_updates = orders_skewed.limit(50).withColumn("amount", col("amount") + 20) order_updates.write.format("delta").mode("overwrite").save("/mnt/delta/retail/order_updates")

delta_table = DeltaTable.forPath(spark, "/mnt/delta/retail/orders") updates_df = spark.read.format("delta").load("/mnt/delta/retail/order_updates")

(delta_table.alias("target") .merge(updates_df.alias("source"), "target.order_id = source.order_id") .whenMatchedUpdateAll() .whenNotMatchedInsertAll() .execute())

COMMAND ----------

Step 4: Optimize and ZORDER

spark.sql("OPTIMIZE delta./mnt/delta/retail/orders ZORDER BY (customer_id)")

COMMAND ----------

Step 5: Time Travel and Audit

print("Latest version") spark.read.format("delta").load("/mnt/delta/retail/orders").show(5)

print("Historical version") spark.read.format("delta").option("versionAsOf", 0).load("/mnt/delta/retail/orders").show(5)

COMMAND ----------

Step 6: Orchestration (Simulated as sequential tasks in notebook)

print("Step 6 completed: Simulate orchestration using workflow or task scheduler like Airflow")
