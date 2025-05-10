### Design a unified batch and streaming data pipeline.

This is called the Lambda Architecture.

Layers:

Batch layer: historical data from S3 using Spark jobs → Delta tables

Speed layer: real-time data using Kafka + Spark Streaming → Delta

Serving layer: query unified Gold layer via Databricks SQL
