# Business Modeling (Gold Layer)

# Model Fact Table and Dimension Table.

# Customer Dimension
customer_dim = spark.sql("""
SELECT DISTINCT customer_id
FROM silver.orders_cleaned
""")

customer_dim.write.format("delta").mode("overwrite").saveAsTable("gold.dim_customer")

# Orders Fact
orders_fact = spark.sql("""
SELECT order_id, order_date, customer_id, order_total, payment_mode
FROM silver.orders_cleaned
""")

orders_fact.write.format("delta").mode("overwrite").saveAsTable("gold.fact_orders")
