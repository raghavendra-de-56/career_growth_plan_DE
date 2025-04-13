## Data Lineage

### What It Is:
Tracking the full journey of data from source to consumption — showing how it's transformed, joined, filtered, and visualized.

### Why It Matters:

1. Impact analysis before schema changes
2. Debugging data quality issues
3. Regulatory audits and compliance
4. Building trust with stakeholders

### Tools:

1. Unity Catalog (native UI for table/column lineage)
2. DataHub, OpenMetadata, Atlan, Collibra
3. dbt lineage graphs

### Use Case:

```
iot_raw.temperature  -->  validated.temperature
                           |
                           --> enriched.temp_celsius
                                   |
                                   --> powerbi_iot_dashboard
```

### Implementation Tips:

1. Use tools with automated lineage capture (Unity Catalog, dbt)
2. Complement with manual annotations for critical flows
3. Version control DAGs and transformations
4. Track schema changes and propagate downstream alerts
