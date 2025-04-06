Databricks + Unity Catalog + Apache Iceberg (Notebook)

This assumes you're using a Unity Catalog-enabled workspace and your cluster has access to the Iceberg table format (which is supported natively on Databricks).


---

Step 0: Define Catalog, Schema, and Table Names

catalog = "your_catalog"          # e.g., "main"
schema = "your_schema"            # e.g., "supply_chain"
table = "iceberg_shoes_brands"    # Your table name
full_table_name = f"{catalog}.{schema}.{table}"


---

Step 1: Create a Table in Iceberg Format

from pyspark.sql.functions import col
from pyspark.sql import Row

data = [
    Row(id=1, brand="Nike", created_date="2024-01-01"),
    Row(id=2, brand="Adidas", created_date="2024-02-15"),
    Row(id=3, brand="Puma", created_date="2024-03-10")
]
df = spark.createDataFrame(data)

# Write to Iceberg table
df.writeTo(full_table_name) \
  .using("iceberg") \
  .tableProperty("format-version", "2") \
  .createOrReplace()


---

Step 2: Query the Iceberg Table

spark.read.table(full_table_name).show()


---

Step 3: Perform an Update (Overwrite Mode with Partition Awareness)

from pyspark.sql.functions import lit

# Update brand to add suffix
updated_df = df.withColumn("brand", col("brand") + " - Updated")

# Append with overwrite mode to simulate update
updated_df.writeTo(full_table_name).overwritePartitions().append()


---

Step 4: Time Travel (Query Historical Data)

# List snapshots
spark.sql(f"SELECT * FROM {full_table_name}.snapshots").show()

# Pick snapshot_id from above and query
snapshot_id = "1234567890"  # Replace with actual ID

historical_df = spark.read.option("snapshot-id", snapshot_id).table(full_table_name)
historical_df.show()
