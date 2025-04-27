# Notebook 5: Schema Drift Detection

# Filename: 4.0_Schema_Drift_Detection.ipynb

# Databricks Notebook - Schema Drift Detection

# Load current schema
current_schema = set([field.name for field in bronze_orders_df.schema.fields])

# Define expected schema
expected_schema = {"order_id", "customer_id", "order_amount", "order_date"}

# Compare schemas
if current_schema != expected_schema:
    print("WARNING: Schema drift detected!")
    print("Expected:", expected_schema)
    print("Found:", current_schema)
    # (Optional) Trigger alert/raise exception
