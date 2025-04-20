Here are some sample interview questions along with answers for Week 3: Data Modeling, Data Contracts, and Schema Evolution — specifically tailored for a Staff Data Engineer role:

What are the key differences between Star Schema, Snowflake Schema, and Data Vault modeling?

Answer:

Star Schema: Central fact table linked to denormalized dimension tables. Simpler and faster for querying.

Snowflake Schema: Normalized dimensions (i.e., dimensions split into sub-dimensions). More space-efficient but slightly complex.

Data Vault: Composed of Hubs (business keys), Links (relationships), and Satellites (context/time-variant data). Ideal for agile and auditable data warehousing.

How do you implement schema evolution in a streaming pipeline using Apache Spark?

Answer:

Use the mergeSchema option while reading/writing with Delta Lake:
```
df.write.format("delta").option("mergeSchema", "true").mode("append").save("/path/to/delta-table")
```
Use ALTER TABLE to add/remove columns if needed.

Maintain schema versions using Unity Catalog or schema registry to track changes and ensure downstream compatibility.

What are data contracts and how do they help with data quality?

Answer:

A data contract is a formal agreement between data producers and consumers specifying the schema, semantics, and SLAs.

They help:

Prevent schema drift

Enforce validation rules

Enable testing with contract-testing frameworks like Pact or Great Expectations

How do you handle Slowly Changing Dimensions (SCD)?

Answer:

SCD Type 1: Overwrite old data (no history maintained).

SCD Type 2: Maintain historical data by creating new rows with effective dates.

SCD Type 3: Maintain limited history in the same row using additional columns (e.g., current and previous).


Example SCD2 with Delta Lake:
```
from delta.tables import *

deltaTable = DeltaTable.forPath(spark, "/mnt/delta/dim_customer")

(deltaTable.alias("target")
 .merge(source_df.alias("source"), "target.customer_id = source.customer_id")
 .whenMatchedUpdate(set={"current_flag": "false", "end_date": "current_date()"})
 .whenNotMatchedInsert(values={"customer_id": "source.customer_id", ...})
 .execute())
```
 What is schema drift and how do you detect and manage it?

Answer:

Schema drift refers to unexpected changes in data structure (e.g., new/missing columns).

Detection:

Compare inferred schema with expected schema using PySpark's StructType

Use tools like Deequ, Great Expectations, or OpenMetadata


Management:

Alert and quarantine offending records

Version schemas using Unity Catalog

Schema Evolution in Real-Time Pipelines — a common area in interviews:

How do you ensure backward and forward compatibility in schema evolution in a real-time Kafka-based pipeline?

Answer:

To manage schema evolution in real-time pipelines, follow these principles:

Use a Schema Registry (e.g., Confluent Schema Registry or Databricks Unity Catalog)

Define compatibility rules:

Backward: New consumers can read old data.

Forward: Old consumers can read new data.

Full: Both forward and backward.


Add only optional fields or fields with default values in schema changes.


Practical Code (PySpark + Kafka + Schema Registry):
```
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import from_json, col

# Step 1: Define expected schema (latest version)
expected_schema = StructType([
    StructField("user_id", StringType()),
    StructField("event_type", StringType()),
    StructField("event_ts", StringType()),
    StructField("device_type", StringType(), True)  # newly added field
])

# Step 2: Read from Kafka topic
df_raw = (spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "<broker>")
    .option("subscribe", "user_events")
    .load())

# Step 3: Deserialize JSON with schema
df_parsed = df_raw.selectExpr("CAST(value AS STRING)").select(
    from_json(col("value"), expected_schema).alias("parsed")
).select("parsed.*")

# Step 4: Optional - Validate schema at runtime
df_parsed.printSchema()
```
Tips for Interview:

Mention Avro + Schema Registry as the most used combo.

Talk about schema evolution testing in CI/CD.

Highlight how you alert on incompatible changes using unit tests or Great Expectations.


### How do you ensure backward and forward compatibility in schema evolution in a real-time Kafka-based pipeline?

Answer:

To manage schema evolution in real-time pipelines, follow these principles:

Use a Schema Registry (e.g., Confluent Schema Registry or Databricks Unity Catalog)

Define compatibility rules:

Backward: New consumers can read old data.

Forward: Old consumers can read new data.

Full: Both forward and backward.

Add only optional fields or fields with default values in schema changes.

Practical Code (PySpark + Kafka + Schema Registry):
```
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import from_json, col

# Step 1: Define expected schema (latest version)
expected_schema = StructType([
    StructField("user_id", StringType()),
    StructField("event_type", StringType()),
    StructField("event_ts", StringType()),
    StructField("device_type", StringType(), True)  # newly added field
])

# Step 2: Read from Kafka topic
df_raw = (spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "<broker>")
    .option("subscribe", "user_events")
    .load())

# Step 3: Deserialize JSON with schema
df_parsed = df_raw.selectExpr("CAST(value AS STRING)").select(
    from_json(col("value"), expected_schema).alias("parsed")
).select("parsed.*")

# Step 4: Optional - Validate schema at runtime
df_parsed.printSchema()
```
Tips for Interview:

Mention Avro + Schema Registry as the most used combo.

Talk about schema evolution testing in CI/CD.

Highlight how you alert on incompatible changes using unit tests or Great Expectations.
