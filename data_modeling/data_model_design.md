1. Multi-Tenancy Data Model Design in a SaaS Platform

Answer:

Options:

Shared schema, tenant ID as a column: Best for simplified schema management and cost-efficiency.

Isolated schema per tenant: Better for strict data isolation and customizations.

Hybrid: Shared schema for common entities + isolated schemas for sensitive/custom data.

Design Principles:

Add tenant_id to every table and enforce row-level security using views or policies (e.g., Unity Catalog row filters).

Use Delta Lake ZORDER on tenant_id for better performance.

2. Schema Compatibility in Kafka Pipelines

Answer:

Schema Evolution Strategy:

Use Avro or Protobuf with a Schema Registry.

Maintain backward or full compatibility.

Add only optional fields or fields with default values.

Tools: Confluent Schema Registry, AWS Glue Schema Registry, Unity Catalog.

3. Handling Schema Drift in Production

Answer:

Detection: Use schema validation tools like Great Expectations or Deequ.

Resolution:

Replay old data into a new schema with mapping.

Use Delta Lake’s schema evolution with versioning.

Prevention:

Enforce schemas at ingestion.

Set up alerts when schema changes are detected.

4. Implementing SCD Type 2 in Delta Lake with Unity Catalog

Approach:
```
from delta.tables import *

deltaTable = DeltaTable.forName(spark, "customer_dim")

updatesDF = spark.read.table("staging_customer_dim")

deltaTable.alias("target").merge(
    updatesDF.alias("source"),
    "target.customer_id = source.customer_id AND target.current_flag = true"
).whenMatchedUpdate(condition="target.hash != source.hash", set={
    "current_flag": "false",
    "end_date": "current_timestamp()"
}).whenNotMatchedInsert(values={
    "customer_id": "source.customer_id",
    "name": "source.name",
    "current_flag": "true",
    "start_date": "current_timestamp()"
}).execute()
```
5. Dimensional Modeling vs Data Vault

When to use:

Use Dimensional Model for stable, report-ready marts.

Use Data Vault for integrating raw enterprise data in a scalable and auditable way.

6. Data Contracts in Data Mesh

Answer:

Who owns them?: Data producers (domain teams) own and publish contracts.

What’s in the contract?

Schema

SLAs (latency, freshness)

Business semantics


Tools:

OpenMetadata, DataHub, Schemata, or protobuf contracts


Enforcement:

Pre-ingestion validation

CI/CD integration

Governance catalog sync

7. Schema Evolution in Partitioned Datasets

Answer:

Partitioned data (e.g., /date=2024-04-01) can contain files with different schemas.

Delta Lake supports schema evolution and enforced schemas:
```
df.write.option("mergeSchema", "true").format("delta").partitionBy("date").save("/path")
```

8. Schema Registry Role

Answer:

Centralized control of schema versions.

Prevent incompatible changes.

Allow rollback.

Integrations:

Kafka, Spark, Flink

Unity Catalog in Databricks for centralized schema governance

9. End-to-End Lineage Tracking

Answer:

Use tools like Unity Catalog, DataHub, or Amundsen.

Use SLA tags and custom metadata to enrich lineage.

Add logging at transformation layer to capture dependencies.

10. Modeling Multi-Fact Tables with Shared Dimensions

Approach:

Create shared dimensions (e.g., Date, Customer, Product).

Facts:

sales_fact, inventory_fact
