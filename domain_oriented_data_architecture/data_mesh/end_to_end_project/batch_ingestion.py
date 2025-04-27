# Batch Data Ingestion (Daily Order Files)

# File format: .csv

# Ingested into Bronze Table without transformation.

# Bronze ingestion
orders_raw_df = spark.read.option("header", True).csv("s3://retail-orders-bucket/daily/orders_*.csv")

orders_raw_df.write.format("delta").mode("append").saveAsTable("bronze.orders_raw")
