# Databricks Autoloader Example
df_auto = (spark.readStream
    .format("cloudFiles")
    .option("cloudFiles.format", "json")
    .load("/mnt/raw/orders/"))

df_auto.writeStream.format("delta").option("checkpointLocation","/mnt/chk/orders/").start("/mnt/delta/orders/")

