# Step 1: Set Iceberg configuration (only needed for non-Databricks Spark setups)
spark.conf.set("spark.sql.catalog.my_catalog", "org.apache.iceberg.spark.SparkCatalog")
spark.conf.set("spark.sql.catalog.my_catalog.type", "hadoop")  # or 'hive' if using HiveCatalog
spark.conf.set("spark.sql.catalog.my_catalog.warehouse", "/tmp/iceberg_warehouse")

# Step 2: Create a sample DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

data = [
    (1, "Nike", "2024-01-01"),
    (2, "Adidas", "2024-02-15"),
    (3, "Puma", "2024-03-10")
]
columns = ["id", "brand", "created_date"]
df = spark.createDataFrame(data, columns)

# Step 3: Write to an Iceberg table
df.writeTo("my_catalog.db.shoes_brands") \
  .using("iceberg") \
  .tableProperty("format-version", "2") \
  .createOrReplace()

# Step 4: Query the Iceberg table
iceberg_df = spark.read.table("my_catalog.db.shoes_brands")
iceberg_df.show()

# Step 5: Perform an Update (requires Spark 3.3+ and Iceberg 1.2+)
from pyspark.sql.functions import lit

update_df = df.withColumn("brand", lit("Nike Updated"))
update_df.writeTo("my_catalog.db.shoes_brands").overwritePartitions().append()

# Step 6: Time Travel - Query previous version (if supported)
# You need to find the snapshot ID first
snapshots_df = spark.sql("SELECT * FROM my_catalog.db.shoes_brands.snapshots")
snapshots_df.show()

# Use one of the snapshot_ids in the query
snapshot_id = snapshots_df.select("snapshot_id").first()["snapshot_id"]

df_snapshot = spark.read.option("snapshot-id", snapshot_id).table("my_catalog.db.shoes_brands")
df_snapshot.show()
