# Enhanced Schema Evolution Simulator

# Imagine new fields like payment_mode, coupon_code suddenly appear in your incoming data!

# Notebook Code: Schema Drift Simulation

# Databricks notebook: schema_evolution_simulator

from pyspark.sql import Row

# Simulating a change - adding new columns
new_data = [
    Row(order_id="123", order_date="2024-04-01", customer_id="C1", order_total=100, payment_mode="Credit Card"),
    Row(order_id="124", order_date="2024-04-02", customer_id="C2", order_total=200, payment_mode="Cash"),
]

# Convert to DataFrame
evolved_df = spark.createDataFrame(new_data)

# Save to Delta (simulate overwrite)
evolved_df.write.format("delta").mode("overwrite").save("/mnt/retail/orders/raw")

print("New fields introduced into the pipeline!")

# Run schema drift detection again!
