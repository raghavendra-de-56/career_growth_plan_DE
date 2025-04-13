## Metadata Management

### What It Is:
Managing and tracking metadata (data about data): schema, usage, ownership, lineage, data quality, etc.

### Types of Metadata:
1. Technical: Schema, format, column names/types
2. Operational: Last updated, freshness, volume, errors
3. Business: Ownership, glossary terms, definitions
4. Social: Who uses it, how often, in which reports

### Key Tools:

1. Unity Catalog (auto metadata capture + APIs)
2. DataHub, Amundsen, OpenMetadata
3. dbt (docs + lineage + ownership metadata)

### Best Practices:

1. Automate metadata extraction (auto cataloging)
2. Embed metadata updates into CI/CD pipelines
3. Enable self-service search via metadata portals
4. Use metadata in pipeline logic (e.g., skip tables not updated in 7 days)
