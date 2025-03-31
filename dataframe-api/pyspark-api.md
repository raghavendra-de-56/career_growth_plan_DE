# Below are the spark Dataframe API available in the pyspark

pyspark.sql.DataFrame.__getattr__

Parameters:name : str
Column name to return as Column.
Returns: Column
      Requested column.
Examples:
```
  df = spark.createDataFrame([
    (2, "Alice"), (5, "Bob")], schema=["age", "name"])
df.select(df.age).show()
```

