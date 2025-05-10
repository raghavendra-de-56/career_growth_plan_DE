# Delta Streaming Read and Write
df_transformed.writeStream.format("delta")
.outputMode("append")
.option("checkpointLocation", "/mnt/chk/enriched_orders/")
.start("/mnt/delta/enriched_orders/")

df_delta_stream = (spark.readStream
    .format("delta")
    .load("/mnt/delta/enriched_orders/"))
