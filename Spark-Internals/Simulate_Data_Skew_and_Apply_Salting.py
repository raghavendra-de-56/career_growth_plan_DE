# Simulate Data Skew and Apply Salting
from pyspark.sql.functions import lit, concat_ws, rand

# Simulate skew by duplicating a single key
skewed_orders = orders.withColumn("customer_id", lit("skewed_customer"))

# Salting technique
salted_orders = skewed_orders.withColumn("salt", (rand() * 10).cast("int"))
salted_orders = salted_orders.withColumn("salted_key", concat_ws("_", "customer_id", "salt"))

# Adjust customers to join on salted key
salted_customers = customers.withColumn("salt", lit(0))
joined = salted_orders.join(salted_customers, salted_orders["salted_key"].contains(salted_customers["customer_id"]))
joined.explain(True)
