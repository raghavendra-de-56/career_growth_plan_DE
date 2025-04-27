## Core Concepts to Master


|Topic | Description |
|------|-------------|
|Principles| Federated governance domain ownership, product thinking for data |
|Data as a product | Each dataset should be treated like a software product (SLAs, APIs, docs)|
|Domain-Oriented Ownership| Each business domain owns its own data pipelines and quality|
|Self-service Infrastructure | Platform team provide tooling for easy onboarding(Databricks, Airflow, Terraform)|
|Federated Computational Governance| Balance between global policies and domain flexibility|

### Data Mesh Four Principles

1. Domain ownership: Data responsibility lies with domain teams.
2. Data as a product: Consumers treated as customers, with clear documentation, SLA.
3. Self-service Platform: Centralized infra team enables others(catalogs, pipelines, CI/CD)
4. Federared Governance: Lightweight rules on security, privacy, observability

Example: 
1. Sales team owns "customer_orders" data product.
2. Marketing team owns "campaign_clicks" product.


### Building Data Products

|Aspect|How to Implement|
|------|----------------|
|Documentation | Schema, SLAs, expected behavior|
|Access APIs| Data available via Delta Tables, REST APIs|
|Quality Guarantees| Validation rules, expectations, uptime commitment|
|Observability| Metrics on freshness, volume, schema drift|



