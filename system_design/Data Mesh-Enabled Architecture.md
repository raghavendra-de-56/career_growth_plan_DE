### Data Mesh-Enabled Architecture

Question:
Design a multi-domain data platform using Data Mesh principles for real-time and batch processing.

Design Components:

Domains: Orders, Customers, Inventory as independent teams

Each domain: owns their own Kafka topics, Delta tables, quality checks, and access controls

Mesh Fabric Layer: Unity Catalog for governance, sharing, and discoverability

Standardization: Use Delta Live Tables with expectations across domains

Data Product: Expose curated Gold tables with SLAs and contracts
