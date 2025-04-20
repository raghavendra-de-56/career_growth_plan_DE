# Data Modeling - SCD Type 2 with Delta Lake
from delta.tables import DeltaTable
from pyspark.sql.functions import current_date

# Sample source data with updated names
source_data = [
    (101, "Alice Smith"),
    (102, "Bob Johnson Updated"),
    (103, "Charlie"),
]
source_df = spark.createDataFrame(source_data, ["customer_id", "customer_name"])

# Load target Delta table
target_table = DeltaTable.forName(spark, "silver.customer_dim")

# Merge source with target using SCD Type 2 logic
target_table.alias("tgt").merge(
    source_df.alias("src"),
    "tgt.customer_id = src.customer_id AND tgt.current = true"
).whenMatchedUpdate(
    condition="tgt.customer_name != src.customer_name",
    set={
        "current": "false",
        "end_date": "current_date()"
    }
).whenNotMatchedInsert(
    values={
        "customer_id": "src.customer_id",
        "customer_name": "src.customer_name",
        "start_date": "current_date()",
        "end_date": "null",
        "current": "true"
    }
).execute()
