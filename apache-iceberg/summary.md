Apache Iceberg is a high-performance table format designed for large-scale analytics datasets. It was originally developed at Netflix and is now an open-source project under the Apache Software Foundation. Iceberg solves many challenges associated with traditional data lake formats like Hive or older Parquet-based tables.

What is a Table Format?

In a data lake, files are typically stored in formats like Parquet or ORC. A table format like Iceberg adds structure and metadata on top of these files so that they can be treated like database tables — enabling features like ACID transactions, schema evolution, and time travel.


---

Key Features of Apache Iceberg

1. ACID Transactions

Supports atomic operations (like insert, update, delete) across large datasets using a metadata layer.

This is something Hive or just raw Parquet doesn't handle well.


2. Schema Evolution

Allows you to add, drop, or rename columns without breaking downstream consumers.

Keeps a full schema history.


3. Partition Evolution

You can change the partitioning of your data over time without rewriting existing data.


4. Hidden Partitioning

Unlike Hive, where you manually define and manage partition columns, Iceberg automatically optimizes partitioning and hides it from query logic.


5. Time Travel

You can query data as of a specific point in time or snapshot, enabling data debugging, audits, and recovery.


6. Optimized for Performance

Iceberg supports features like metadata pruning, file pruning, and vectorized reads, which make queries faster compared to traditional Hive tables.



---

Architecture Overview

Manifest Files: List data files and metadata.

Manifest Lists: Point to manifest files (like an index).

Snapshot: A pointer to a manifest list.

Table Metadata: Contains snapshot references, schema versions, and partition info.


So when you query an Iceberg table, it uses the latest snapshot, finds the relevant files via manifests, and reads only what is necessary.


---

Iceberg vs Delta Lake vs Hudi


---

Popular Use Cases

Data lakes that need database-like features.

Large-scale batch and streaming ingestion with transactional guarantees.

Data mesh or data product architectures where each team manages its own tables.



---

Tools that Support Iceberg

Query engines: Trino, Presto, Spark, Flink, Dremio, Snowflake.

Data platforms: AWS Athena, Snowflake, Cloudera, Databricks (recent support with Unity Catalog), Starburst.
