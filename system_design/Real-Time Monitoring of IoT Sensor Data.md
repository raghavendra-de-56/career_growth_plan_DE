### Real-Time Monitoring of IoT Sensor Data

Question:
Design a system to collect, monitor, and alert based on real-time IoT sensor streams from 100,000 devices sending data every few seconds.

Solution Highlights:

Kafka or MQTT brokers for ingestion

Spark Structured Streaming with sliding windows + watermarking

Delta Bronze for raw logs, Silver for filtered data (outlier removal, null cleanup)

Gold layer for aggregations: hourly/daily summaries per device

Custom alerts pushed to Kafka or REST APIs when thresholds are breached

Use DLT with expectations for continuous quality monitoring


Code for outlier detection example:
```
from pyspark.sql.functions import col, mean, stddev

stats = df.groupBy("device_id").agg(mean("temperature").alias("avg"), stddev("temperature").alias("std"))
df_filtered = df.join(stats, "device_id").filter((col("temperature") > col("avg") - 2*col("std")) & 
                                                 (col("temperature") < col("avg") + 2*col("std")))
```
