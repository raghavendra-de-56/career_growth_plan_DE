Slowly Changing Dimensions (SCDs) are key concepts in dimensional modeling, especially important in data warehousing and ETL pipelines. They handle how changes in dimension data (like customer info, product details) are tracked over time.

What Are Slowly Changing Dimensions (SCDs)?

SCDs are dimensions that change slowly over time, rather than frequently (like fact data). 

For example:

A customer’s address or marital status might change.

A product description or category might get updated.

There are three most common types:

### Type 1 – Overwrite (No History)

Use Case:

When you don’t care about history of the data. You just want the latest value.

Example:

If a customer changes their address, just update the value.

If Alice moves to LA:

UPDATE directly:
```
UPDATE dim_customer
SET address = 'LA, USA'
WHERE customer_id = 1001;
```
Pros:

Simple

No storage overhead

Cons:

No history of previous values

Not good for audit/tracking

### Type 2 – Add New Row (Keep Full History)

Use Case:

When you want to track historical changes.

Example:

If a customer changes address, insert a new row with a new surrogate key and effective date range.

Insert new row:
```
INSERT INTO dim_customer (sk_customer, customer_id, name, address, is_current, effective_date)
VALUES (3, 1001, 'Alice Smith', 'LA, USA', 'Y', current_date());
```
Pros:

Full historical tracking

Great for auditing and time-based analysis

Cons:

More storage

Logic is more complex

Needs surrogate keys and valid date ranges

### Type 3 – Add New Column (Limited History)

Use Case:

When you want to store limited historical values, such as the current and previous value.

Example:

Keep both the current address and the previous address in the same row.

UPDATE with shift:
```
UPDATE dim_customer
SET previous_address = current_address,
    current_address = 'LA, USA'
WHERE customer_id = 1001;
```
Pros:

Tracks limited history

Simpler than Type 2

Cons:

Only one previous version stored

Can’t track full history

### Real-World Scenario in Databricks (PySpark – Type 2)

Here’s how you might implement SCD Type 2 in a Databricks using Delta Lake:
```
from pyspark.sql.functions import col, current_date, lit

# Incoming data (latest updates)
incoming_df = spark.read.table("staging_customer")

# Existing dim table
dim_df = spark.read.table("dim_customer")

# Find changed records
changed = dim_df.alias("dim").join(
    incoming_df.alias("stage"),
    on="customer_id"
).filter("dim.address != stage.address AND dim.is_current = 'Y'")

# Expire old records
expired = changed.withColumn("expiry_date", current_date()) \
                 .withColumn("is_current", lit("N"))

# New version of records
new_records = changed.select(
    "customer_id", "name", "stage.address"
).withColumn("is_current", lit("Y")) \
 .withColumn("effective_date", current_date()) \
 .withColumn("expiry_date", lit(None).cast("date"))

# Merge everything
final_df = dim_df.unionByName(expired).unionByName(new_records)

final_df.write.format("delta").mode("overwrite").saveAsTable("dim_customer")
```

