# Deduplication and Idempotent Streaming Write
df_deduped = df.dropDuplicates(["order_id", "order_time"])

df_deduped.writeStream
          .format("delta")
          .option("checkpointLocation", "/mnt/chk/deduped/")
          .start("/mnt/delta/orders_deduped/")
