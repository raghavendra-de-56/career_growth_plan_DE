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
