# Delta Live Tables (DLT) Production Pipeline

# Instead of custom jobs, Databricks Delta Live Tables (DLT) helps manage data quality, auto-lineage, and reliability.

# Bronze Layer DLT Table

# bronze_orders_dlt.py

from dlt import table
import pyspark.sql.functions as F

@table
def bronze_orders_batch():
    return (
        spark.read.format("csv")
        .option("header", "true")
        .load("s3://your-retail-data/bronze/orders/")
    )

# Silver Layer DLT Table

# silver_orders_dlt.py

from dlt import table

@table
def silver_orders_validated():
    df = dlt.read("bronze_orders_batch")
    
    return (
        df.filter("order_id IS NOT NULL AND customer_id IS NOT NULL")
          .withColumn("order_date", F.to_date("order_date", "yyyy-MM-dd"))
          .withColumn("order_total", F.col("quantity") * F.col("unit_price"))
    )

# Gold Layer DLT Table

# gold_sales_fact_dlt.py

from dlt import table

@table
def fact_sales_summary():
    df = dlt.read("silver_orders_validated")
    
    return (
        df.groupBy("customer_id")
          .agg(
              F.sum("order_total").alias("total_spent"),
              F.count("order_id").alias("total_orders")
          )
    )
