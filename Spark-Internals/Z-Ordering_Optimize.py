# 4. Z-Ordering and Optimize
spark.sql("OPTIMIZE delta./mnt/delta/orders ZORDER BY (customer_id)")
