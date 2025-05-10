# Kafka Streaming Ingestion
from pyspark.sql.functions import expr

df_kafka = (spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "broker1:9092")
    .option("subscribe", "orders_topic")
    .option("startingOffsets", "latest")
    .load())

df_parsed = df_kafka.selectExpr("CAST(value AS STRING)")
