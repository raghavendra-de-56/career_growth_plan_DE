# Watermarking and Late Data Handling
from pyspark.sql.functions import window, to_timestamp

df = df.withColumn("event_time", to_timestamp("order_time"))
aggregated = df.withWatermark("event_time", "10 minutes")
              .groupBy(window("event_time", "5 minutes"))
              .count()
