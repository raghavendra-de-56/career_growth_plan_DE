## Data Governance

### What It Is:
Processes, policies, and technologies that ensure data is secure, compliant, and accessible to the right users.

### Key Governance Pillars:

1. Data Access Control: Role-based access (RBAC/ABAC)
2. Column-Level Security: Restrict sensitive fields (e.g., PII, PHI)
3. Data Classification & Tagging
4. Audit Logging
5. Data Retention Policies
6. Data Sharing Policies (internal & external)


### Tools:

1. Unity Catalog (Databricks)
2. AWS Lake Formation, Azure Purview
3. Collibra, Alation, Immuta

### Real-World Scenarios:

1. Only HR team can access salary and name columns
2. Apply GDPR tagging and retention rules on user data
3. Enable secure cross-account data sharing using Unity Catalog or Delta Sharing

### Databricks Unity Catalog Example:
```
-- Restrict column access
GRANT SELECT (device_id, temperature) ON TABLE iot_data TO iot_analyst;

-- Tag column as PII
ALTER TABLE iot_data ALTER COLUMN device_id SET TAGS ('pii' = 'true');
```

## Design, implement, and evangelize goverance.

### Core Pillars of Data Governance

#### Access Control
Who can read/write data and at what granularity (table/column/row)?

#### Data Classification
What type of data is it(PII, PHI, sensitive, financial, etc)?

#### Audit & Lineage
Who queried/modified the data, and where did the data come from?

#### Policy Enforecement
Ensure consistent tagging, encryption, retention across pipelines

#### Data Quality checks
Ensure freshness, accuracy, completeness, and consistency

#### Data Cataloging 
Maintain searchable, tagged, documented datasets and owners

### Architecture Overview
```
┌────────────────────────────┐
            │        Unity Catalog       │
            │ ─ Tags, ACLs, Lineage UI   │
            │ ─ Data Ownership & Glossary│
            └────────────────────────────┘
                       │
      ┌────────────────┴────────────────┐
      │                                 │
[ Raw Zone (S3/ADLS)]          [ Delta Live Tables / Spark Jobs ]
      │                                 │
[ Validated Zone ]          ──►  Quality Check Rules (Deequ/dbt)
      │
[ Secure Curated Zone ] ──► Masking / RBAC / Data Sharing
      │
[ BI Dashboards / ML Models ]
```

### Hands-On Code Examples with Unity Catalog

#### Set Up Access Control

Example: Table-Level Access Control
```
-- Grant SELECT on the entire table to analysts
GRANT SELECT ON TABLE supply_chain.orders TO analyst_group;

Column-Level Security (CLS):

-- Allow analysts to only see certain columns
GRANT SELECT(order_id, product_id, order_date)
ON TABLE supply_chain.orders
TO analyst_group;
```

#### Data Tagging and Classification

Apply Tags using Unity Catalog:
```
-- Mark sensitive column
ALTER TABLE supply_chain.customers
ALTER COLUMN email
SET TAGS ('sensitivity' = 'PII', 'classification' = 'confidential');

Query Tagged Metadata:

-- Find all columns tagged as PII
SHOW COLUMNS FROM supply_chain.customers
WHERE TAGS['sensitivity'] = 'PII';
```
#### Data Masking Strategy

While Unity Catalog doesn't natively support dynamic masking, combine with view-based masking:
```
-- Create a masked view for PII
CREATE OR REPLACE VIEW secure_customers AS
SELECT
  customer_id,
  CASE
    WHEN current_user() IN ('admin_user', 'auditor') THEN email
    ELSE 'MASKED'
  END AS email,
  country
FROM supply_chain.customers;
```

#### Enforcing Retention & Lifecycle

Manage retention for GDPR/CCPA compliance:
```
-- Create an external table with defined retention (simulate via partitioning)
CREATE TABLE supply_chain.orders_retention
USING DELTA
LOCATION '/mnt/data/orders'
PARTITIONED BY (retention_date);

-- Schedule job to delete expired data
DELETE FROM supply_chain.orders_retention
WHERE retention_date < current_date();

```

#### Data Sharing & Auditing

Enable Delta Sharing (cross-org):
```
-- Share table externally with governance
CREATE SHARE vendor_share;
ALTER SHARE vendor_share ADD TABLE supply_chain.shipments;

-- Grant access to external recipient
CREATE RECIPIENT vendor_team USING IDENTITY 'email@partner.com';
GRANT USAGE ON SHARE vendor_share TO RECIPIENT vendor_team;
```
Audit Logs (in Unity Catalog or CloudTrail):

Track GRANT, SELECT, CREATE, ALTER via Unity Catalog audit logs.

Pipe logs to Lakehouse or use Databricks audit log APIs.

### Real-World Scenario

#### Context:

You manage product forecast and inventory datasets.

Access is needed across regions (US, EU), but with restrictions on customer-related fields.

Governance Solution:
1. Tag customer_email and address columns as PII
2. Restrict PII fields to only EU_Privacy_Team
3. Enforce RBAC using Unity Catalog group policies
4. Share forecast data with partners using Delta Sharing
5. Implement view masking for analysts
6. Schedule data retention cleanup every 90 days
