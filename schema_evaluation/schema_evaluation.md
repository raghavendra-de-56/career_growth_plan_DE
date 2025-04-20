### Schema Evaluation:

Schema evaluation in data engineering refers to the process of assessing and validating the structure and organization of data, typically defined by a schema. This involves checking the schema's correctness, completeness, and consistency to ensure it meets the requirements of the application or system.

### Key Aspects of Schema Evaluation:

1. Schema Validation: Verifying that the schema conforms to a specific format or standard (e.g., JSON, Avro, or Protobuf).
2. Data Type Checking: Ensuring that the data types defined in the schema match the actual data types of the values.
3. Field Existence and Order: Verifying that all required fields are present and in the correct order.
4. Data Constraints: Checking that data constraints, such as nullability or uniqueness, are correctly defined and enforced.
5. Schema Evolution: Evaluating how changes to the schema will impact existing data and applications.

#### Benefits of Schema Evaluation:

1. Improved Data Quality: Schema evaluation helps ensure that data is accurate, complete, and consistent.
2. Reduced Errors: By validating the schema, you can catch errors early in the development process, reducing the likelihood of downstream issues.
3. Increased Efficiency: Schema evaluation can help automate data processing and integration tasks, improving overall efficiency.
4. Better Data Governance: Schema evaluation promotes data governance by ensuring that data is properly defined, documented, and managed.

#### Tools for Schema Evaluation:

1. Schema definition languages (e.g., JSON Schema, Avro Schema).
2. Data validation libraries (e.g., JSON Validator, Avro Validator).
3. Data governance platforms (e.g., Collibra, Informatica).

By evaluating and validating schemas, data engineers can ensure that their data is well-structured, reliable, and meets the requirements of their applications and systems.

### Concepts to Learn:

1. Delta Lake's schema evolution modes: mergeSchema, overwriteSchema
2. Backward/Forward Compatibility
3. Upstream schema drift: how to detect, validate, and alert

### Tooling:

1. Delta Lake
2. Apache Iceberg / Apache Hudi (optional)
3. Databricks Unity Catalog schema versioning

### Hands-on Examples:
```
# Automatically evolve schema during write
df.write.format("delta") \
  .mode("append") \
  .option("mergeSchema", "true") \
  .saveAsTable("bronze.sales")
```

### Schema Drift Detection Strategy:

1. Compare incoming schema using df.schema.json() with expected schema
2. Raise alert/log to a Slack channel or ticketing system

### Schema Evolution in Delta Lake
```
# Original schema
df1 = spark.createDataFrame([(1, "Product A")], ["product_id", "product_name"])
df1.write.format("delta").mode("overwrite").saveAsTable("bronze.products")

# Evolved schema with new column
df2 = spark.createDataFrame([(2, "Product B", "Electronics")], ["product_id", "product_name", "category"])
df2.write.option("mergeSchema", "true").format("delta").mode("append").saveAsTable("bronze.products")
```

### What Is Schema Drift?

Schema drift happens when the structure (schema) of incoming data changes unexpectedly. 

For example:
1. A new column appears
2. A column is removed or renamed
3. A data type is changed

If not handled, it can break pipelines, corrupt data, or affect downstream analytics.

### Why Is Schema Drift Detection Important?

1. Ensures backward compatibility
2. Prevents pipeline failures or silent data corruption
3. Maintains trust in analytics and ML outputs

### Schema Drift Detection with PySpark + Delta Lake (Batch)
```
from pyspark.sql.types import StructType
import json

# Step 1: Define your expected schema (can be loaded from config or schema registry)
expected_schema = StructType().add("id", "int").add("name", "string")

# Step 2: Read the incoming file
incoming_df = spark.read.option("header", True).csv("/mnt/data/new_data.csv")

# Step 3: Capture the incoming schema
incoming_schema = incoming_df.schema

# Step 4: Compare
if expected_schema != incoming_schema:
    print("SCHEMA DRIFT DETECTED!")
    print("Expected Schema:\n", expected_schema.simpleString())
    print("Incoming Schema:\n", incoming_schema.simpleString())
    # Log, send alert, or halt the pipeline here
else:
    print("Schema matches. Continue processing.")
```

### Schema Drift Detection with Streaming Data (Structured Streaming)
```
from pyspark.sql.streaming import DataStreamReader
from pyspark.sql.functions import col

# Reference schema (load from previous schema snapshot)
expected_schema = StructType().add("device_id", "string").add("temperature", "double")

# Ingest streaming data
stream_df = spark.readStream.option("header", True).schema(expected_schema).csv("/mnt/streaming/iot")

# Step 1: Read file header separately to detect schema
sample_df = spark.read.option("header", True).csv("/mnt/streaming/iot")

if sample_df.schema != expected_schema:
    print("SCHEMA DRIFT in streaming source!")
    # Store the schema difference, raise alert
```

### Advanced: Schema Drift Tracking & Logging

You can persist schema versions into Delta Lake or a metadata table.
```
from datetime import datetime

# Save current schema version
schema_json = json.dumps(incoming_df.schema.jsonValue())

audit_df = spark.createDataFrame([
    (datetime.now().isoformat(), schema_json)
], ["ingestion_time", "schema_json"])

audit_df.write.format("delta").mode("append").saveAsTable("audit.schema_versions")
```
Unity Catalog schema versioning is an advanced feature that helps you track changes to table schemas over time, ensuring auditability, data quality, and traceability—especially important for building production-grade systems.

### What Is Schema Versioning in Unity Catalog?

Unity Catalog doesn't have native "schema versioning" like Git, but you can implement schema version tracking manually using:
1. Unity Catalog table metadata
2. Delta Lake transaction logs
3. Custom schema audit tables
4. Table history (DESCRIBE HISTORY)

### Use Unity Catalog Table History

Delta tables (managed by Unity Catalog) log all schema changes.
```
DESCRIBE HISTORY main.sales.retail_orders;
```
This will show you:
1. Operation (e.g., ALTER TABLE ADD COLUMN)
2. User who made the change
3. Timestamp
4. Notebook or job that initiated it

### Extract and Store Schema Versions Over Time (PySpark)
```
from pyspark.sql.types import StructType
import json
from datetime import datetime

# Step 1: Load the current schema from Unity Catalog table
table_name = "main.sales.retail_orders"
df = spark.table(table_name)
schema_json = json.dumps(df.schema.jsonValue())

# Step 2: Create an audit table if not exists
spark.sql("""
CREATE TABLE IF NOT EXISTS main.audit.schema_versions (
  table_name STRING,
  schema_json STRING,
  schema_hash STRING,
  captured_at TIMESTAMP
) USING DELTA
""")

# Step 3: Calculate schema hash to detect change
import hashlib
schema_hash = hashlib.md5(schema_json.encode("utf-8")).hexdigest()

# Step 4: Insert schema version into audit table
audit_df = spark.createDataFrame([
    (table_name, schema_json, schema_hash, datetime.now())
], ["table_name", "schema_json", "schema_hash", "captured_at"])

audit_df.write.mode("append").format("delta").saveAsTable("main.audit.schema_versions")
```

View Schema Change History
```
SELECT * FROM main.audit.schema_versions
WHERE table_name = 'main.sales.retail_orders'
ORDER BY captured_at DESC;
```
Compare Schema Versions

You can extract two versions and use Python to compare:

###  Compare two schema versions
```
schema1 = json.loads(df1.schema_json)
schema2 = json.loads(df2.schema_json)

from deepdiff import DeepDiff
diff = DeepDiff(schema1, schema2, ignore_order=True)
print(diff)
```
