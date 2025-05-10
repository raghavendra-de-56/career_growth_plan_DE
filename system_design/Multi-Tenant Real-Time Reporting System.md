### Scenario: Multi-Tenant Real-Time Reporting System

Question:
How would you design a multi-tenant reporting system for 100+ enterprise customers with isolated data and real-time dashboards?

Key Concepts:

Kafka → Spark → Delta Lake architecture

Row-level security using Unity Catalog + dynamic views

Schema-per-tenant or attribute-based filtering

Use Delta Sharing or Databricks SQL with fine-grained ACLs

Metadata tagging for tenant-specific lineage and governance

Daily backfills for each tenant using structured batch pipelines
