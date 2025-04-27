# Notebook 4: Business Modeling (Gold Layer)

# Filename: 3.0_Business_Modeling.ipynb

# Databricks Notebook - Gold Layer

silver_orders_df = spark.read.format("delta").load("/mnt/datalake/silver/orders/")

# Create aggregate sales fact table
sales_fact_df = silver_orders_df.groupBy("customer_id").agg(
    {"order_amount": "sum"}
).withColumnRenamed("sum(order_amount)", "total_sales")

sales_fact_df.write.format("delta") \
    .mode("overwrite") \
    .save("/mnt/datalake/gold/fact_sales/")

# Dimension Table (Customer Orders)
customer_orders_dim = silver_orders_df.select("order_id", "customer_id", "order_date")

customer_orders_dim.write.format("delta") \
    .mode("overwrite") \
    .save("/mnt/datalake/gold/dim_customer_orders/")
