# Simulating Schema Drift Detection
# In Staff Data Engineer interviews, they often ask:
# "How would you detect schema drift early in your pipelines?"
# Here's how you can build it:

# Spark Code for Schema Drift Check

from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# Expected schema definition
expected_schema = StructType([
    StructField("order_id", StringType(), True),
    StructField("order_date", StringType(), True),
    StructField("customer_id", StringType(), True),
    StructField("order_total", IntegerType(), True),
])

# Load latest raw data
raw_df = spark.read.format("delta").load("/mnt/retail/orders/raw")

# Get actual schema
actual_schema = raw_df.schema

# Compare schemas
def compare_schemas(expected, actual):
    expected_fields = set((field.name, field.dataType.simpleString()) for field in expected.fields)
    actual_fields = set((field.name, field.dataType.simpleString()) for field in actual.fields)
    
    missing_fields = expected_fields - actual_fields
    new_fields = actual_fields - expected_fields
    
    return missing_fields, new_fields

missing, new = compare_schemas(expected_schema, actual_schema)

if missing or new:
    print("Schema drift detected!")
    print(f"Missing fields: {missing}")
    print(f"New fields: {new}")
    # You can raise alerts or stop pipelines here
else:
    print("No schema drift detected. Safe to proceed.")

# How this helps:

# Proactively detects unexpected columns added/removed
# Helps avoid pipeline failures after schema changes
# Auto alert your DataOps or Engineering team!
