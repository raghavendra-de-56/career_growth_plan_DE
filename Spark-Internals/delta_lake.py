# Delta Lake: Time Travel, Merge, Schema Evolution
from delta.tables import *

# Write a Delta Table
orders.write.format("delta").mode("overwrite").save("/mnt/delta/orders")

# Time travel
spark.read.format("delta").option("versionAsOf", 0).load("/mnt/delta/orders").show()

# Merge (Upsert)
delta_table = DeltaTable.forPath(spark, "/mnt/delta/orders")
updates = spark.read.parquet("/mnt/data/orders_update.parquet")

(delta_table.alias("target")
 .merge(updates.alias("source"), "target.order_id = source.order_id")
 .whenMatchedUpdateAll()
 .whenNotMatchedInsertAll()
 .execute())
