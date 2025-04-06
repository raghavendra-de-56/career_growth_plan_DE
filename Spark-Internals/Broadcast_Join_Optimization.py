# Broadcast Join Optimization
from pyspark.sql.functions import broadcast

customers = spark.read.parquet("/mnt/data/customers.parquet")
orders = spark.read.parquet("/mnt/data/orders.parquet")

# Broadcast the smaller 'customers' DataFrame
optimized_join = orders.join(broadcast(customers), "customer_id")
optimized_join.explain(True)

