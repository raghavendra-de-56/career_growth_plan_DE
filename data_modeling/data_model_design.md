### Multi-Tenancy Data Model Design in a SaaS Platform

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

### Designing Data Models for Shared Dimensions (e.g., User Dimension)

Question:

You need to support multiple product teams consuming a shared user dimension. How do you design the data model to support governance, versioning, and schema evolution?

Answer:

Key Considerations:

Domain Ownership: Define ownership (e.g., Customer Data Platform team).

Data Contracts: Use contract-first design to define what attributes are exposed to consumers.

Schema Versioning: Maintain version-controlled schemas (e.g., via Unity Catalog or Schema Registry).

Backward Compatibility: Use additive changes; avoid dropping/changing types.

Column Lineage & Auditing: Track provenance of fields like email, country, etc.

Architecture:

Store the user dimension as a Delta Table under Unity Catalog.

Use an internal Gold layer for curated full user info.

Expose a subset of attributes through views or materialized tables for each consuming team.

Example in PySpark:
```
# Add new attribute with versioning
from pyspark.sql.functions import current_timestamp

user_df = (
    raw_user_df
    .withColumn("ingestion_ts", current_timestamp())
    .withColumn("version", lit(2))  # Example: version field
)

user_df.write.format("delta").mode("overwrite").saveAsTable("gold.user_dim_v2")
```
What Interviewers Look For:

Thought process around ownership and breaking silos.

How you manage change over time without disrupting consumers.

Real examples of versioning and contracts.
 
### Modeling for GDPR Compliance

Question:
How would you model data to support GDPR compliance (e.g., deletion, user consent, audit trails)?

Answer:

Modeling Techniques:

PII Isolation: Store PII (email, phone) in a separate table with controlled access.

Soft Deletes: Maintain a deleted_flag to logically remove user data.

Consent Table: Model consent as a dimension (user_id, consent_type, timestamp).

Delta Lake Change Data Feed (CDF): Use for tracking changes and deletions.

Tagging & Row-Level Access: Unity Catalog provides masking policies and column-level tags.


Example in PySpark:
```
# GDPR-compliant delete
from delta.tables import DeltaTable

user_table = DeltaTable.forName(spark, "gold.user_dim")
user_table.delete("user_id = 'abc123'")  # Actual deletion when required

# Consent tracking
consent_df = spark.createDataFrame([
    {"user_id": "abc123", "consent_type": "email_marketing", "timestamp": "2024-04-01"}
])
consent_df.write.mode("append").saveAsTable("gold.user_consent_dim")
```
What Interviewers Look For:

Awareness of compliance requirements.

How you've designed models to delete, mask, or restrict sensitive data.

### 3. Multi-Fact Star Schema Design

Question:

What’s your approach to multi-fact schemas? Can you walk through a case where you used bridge tables or conformed dimensions?

Answer:

Use Case:

You have sales_fact (daily sales) and inventory_fact (stock levels).

Both reference the product_dim, but with different granularities.

Design Strategy:

Conformed Dimensions: Shared product_dim, location_dim, etc.

Bridge Tables: Use when many-to-many exists (e.g., product-campaign relationships).

Aggregation Handling: Model grain explicitly — e.g., sales_fact is daily, inventory_fact is hourly.

Example Star Schema:
```
            +--------------+
            | product_dim  |
            +--------------+
                  |
     +------------+-----------+
     |                        |
+------------+         +----------------+
| sales_fact |         | inventory_fact |
+------------+         +----------------+
```
What Interviewers Look For:

Modeling multiple business processes in one warehouse.

Handling dimensional consistency across facts.
