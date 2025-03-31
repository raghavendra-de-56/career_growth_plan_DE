Apache Spark is a distributed computing framework optimized for big data processing. Understanding its internals helps in performance tuning, debugging, and architectural decisions

## Spark Architecture Overview

### Spark Components

#### Driver Program:
  1. The main entry point for Spark applications.
  2. It submits jobs, distributes tasks, and monitors execution.
  
#### Cluster Manager:

  1. Manages resource allocation (CPU, memory) across worker nodes.
  2. Can be YARN, Kubernetes, Mesos, or Standalone.

#### Executor:

  1. Runs on worker nodes and executes tasks.
  2. Each executor has its own memory and caches data locally.

#### Task:

  1. A unit of execution sent to an executor.
  2. Multiple tasks form a stage, and multiple stages form a job.

#### RDD (Resilient Distributed Dataset):

  1. Spark’s fundamental immutable distributed data structure.
  2. Supports transformations (map, filter) and actions (count, collect).

### Architecture Flow:

  1. Driver creates an RDD and triggers an action.
  2. SparkContext translates this into a DAG (Directed Acyclic Graph).
  3. DAG Scheduler breaks the DAG into stages.
  4. Task Scheduler assigns tasks to executors.
  5. Executors execute tasks in parallel and store intermediate data.
  6. Final output is sent back to the driver.

### Spark Execution Flow:

1. DAG (Directed Acyclic Graph)
2. Spark lazily evaluates transformations and builds a DAG before execution.
3. DAG helps optimize execution by reordering operations and reducing shuffles.


Example DAG for a Spark Job
```
df = spark.read.csv("data.csv")  # Stage 1: Read data
df = df.filter(df["col1"] > 100)  # Stage 2: Filter transformation (lazy)
df = df.groupBy("col2").count()  # Stage 3: GroupBy (causes shuffle)
df.show()  # Action triggers execution
```
### DAG Optimization:

1. Stage Splitting: Divides DAG into narrow and wide transformations.
2. Pipeline Execution: Executes multiple operations in a single stage.
3. Shuffle Optimization: Reduces expensive data movement between nodes.

#### Catalyst Optimizer

What is Catalyst Optimizer?

Spark SQL’s query optimizer that improves performance by:

  1. Reordering joins
  2. Predicate pushdown
  3. Column pruning
  4. Cost-based optimizations

Example: Analyzing a Query Plan
```
df = spark.read.parquet("data.parquet")
df_filtered = df.filter(df["col1"] > 100)
df_filtered.explain(True)  # Shows Optimized Execution Plan
```
Execution Plan Breakdown

== Physical Plan ==
Filter (col1 > 100)  -- Predicate Pushdown
Scan parquet data    -- Column Pruning

Predicate Pushdown: Filters applied before reading data, reducing I/O.

Column Pruning: Only loads required columns to save memory.

### Tungsten Engine

#### What is Tungsten?

1. Spark’s memory management engine that optimizes CPU efficiency.
2. Uses off-heap memory, cache-aware computation, and bytecode generation.

#### Tungsten Features
1. Binary Processing: Data is stored in binary format (not JVM objects).
2. Bytecode Generation: Converts queries into Java bytecode at runtime.
3. Off-Heap Memory: Reduces JVM garbage collection overhead.
4. Cache-Aware Computations → Uses CPU registers efficiently.


### Spark Shuffling & Partitioning:

#### What is Shuffling?

Shuffle happens when data moves across nodes, typically in:
1. GroupBy operations
2. Joins (except Broadcast joins)
3. Repartitioning

Shuffle can be expensive due to network & disk I/O.

#### How to Reduce Shuffle?

1. Use Broadcast Joins for Small Tables
```
from pyspark.sql.functions import broadcast
df_large.join(broadcast(df_small), "id")  # Avoids shuffle
```
2. Optimize Partitioning
```
df = df.repartition(10, "col1")  # Repartition based on a column
```
Broadcast Joins Optimization

1. Spark shuffles data for large joins, causing slowness.
2. Use broadcast() when joining a small lookup table to avoid shuffle.


🔹 Example: Optimized Join Using Broadcast
```
from pyspark.sql.functions import broadcast
df_large = spark.read.parquet("large_data.parquet")
df_small = spark.read.parquet("small_lookup.parquet")
df_optimized = df_large.join(broadcast(df_small), "id")  # Avoids shuffle
```
#### Spark Storage Levels (Cache & Persist)

Cache vs. Persist

.cache(): Stores DataFrame only in memory.

.persist(StorageLevel): Allows fine-grained control (MEMORY_AND_DISK, DISK_ONLY, etc.).

Example: Using Cache & Persist
```
df_cached = df.cache()
df_cached.count()  # Materializes cache
```
```
df_persisted = df.persist()
df_persisted.count()
```
 Storage Levels | Storage Level| Memory | Disk | Serialized | 
 
 |----------------------  |--------|------|------------| 
 
 | MEMORY_ONLY            | ✅     | ❌   | ❌         | 
 
 | MEMORY_AND_DISK        | ✅     | ✅   | ❌         | 
 
 | MEMORY_ONLY_SER        | ✅     | ❌   | ✅         | 
 
 | DISK_ONLY              | ❌     | ✅   | ✅         |

#### Spark File Formats & Optimization

Best File Formats for Spark

Convert CSV to Parquet
```
df.write.mode("overwrite").parquet("data.parquet")
```
#### Avoiding Performance Bottlenecks

Avoiding UDFs (User-Defined Functions)

UDFs slow down execution since they don’t benefit from Catalyst Optimizer.

Use Spark’s built-in functions instead of UDFs whenever possible.

Example: Avoid UDFs & Use Built-in Functions


Avoid slow UDFs

```
from pyspark.sql.functions import length
def text_length(text):
    return len(text)
df = df.withColumn("text_length", length(df["text"]))  # Optimized
```

## Understanding DAG & Execution Plan

Goal: Visualize the DAG and analyze query execution plans.

Exercise 1: Basic DAG Execution
```
df = spark.range(1, 1000000)  # Create a DataFrame with 1M rows
df = df.withColumnRenamed("id", "value")
df_filtered = df.filter(df["value"] % 2 == 0)  # Filter even numbers

df_filtered.explain(True)  # Show Execution Plan
df_filtered.count()  # Action triggers execution
```
Key Takeaways:

1. Observe logical & physical execution plans.
2. Check how Spark optimizes lazy transformations.


## Catalyst Optimizer & Predicate Pushdown

Goal: Optimize queries using predicate pushdown.

Exercise 2: Predicate Pushdown in Parquet
```
df = spark.read.parquet("/databricks-datasets/nyctaxi/tripdata/parquet/")
df_filtered = df.filter(df["passenger_count"] > 2)

df_filtered.explain(True)  # Check predicate pushdown
df_filtered.show()
```
Key Takeaways:

1. Look for "PushedFilters" in the explain output.
2. Predicate pushdown reduces data read size.

## Shuffle Optimization with Broadcast Joins

Goal: Use broadcast joins to reduce shuffle.

Exercise 3: Broadcast Join Example
```
from pyspark.sql.functions import broadcast

df_large = spark.range(1, 100000000).withColumnRenamed("id", "large_id")  # Large Dataset
df_small = spark.range(1, 1000).withColumnRenamed("id", "small_id")  # Small Dataset

# Without Broadcast - Causes Shuffle
df_joined = df_large.join(df_small, df_large.large_id == df_small.small_id)
df_joined.explain(True)  # Check if shuffle happens

# With Broadcast - Avoids Shuffle
df_broadcasted = df_large.join(broadcast(df_small), df_large.large_id == df_small.small_id)
df_broadcasted.explain(True)  # Check if shuffle is avoided
```
Key Takeaways:

1. Check BroadcastHashJoin in explain(), indicating shuffle avoidance.

## Partitioning for Performance Optimization

Goal: Improve query performance using partitioning.

Exercise 4: Repartitioning Data
```
df = spark.range(1, 1000000).withColumnRenamed("id", "value")

# Default Partition Count
print(df.rdd.getNumPartitions())

# Increase Partitions (More Parallelism)
df_repartitioned = df.repartition(10)  # Increase partitions
print(df_repartitioned.rdd.getNumPartitions())

# Write Data with Partitioning
df.write.partitionBy("value").parquet("/tmp/partitioned_data")
```
Key Takeaways:
1. Increasing partitions can improve parallelism (but avoid too many).
2. Partitioning large tables reduces scan time.

## Tungsten Engine & Memory Optimization

Goal: Experiment with cache vs persist for memory management.

Exercise 5: Cache vs Persist Performance

from pyspark.storagelevel import StorageLevel
```
df = spark.range(1, 50000000).withColumnRenamed("id", "value")

# Cache (Stored in Memory)
df_cached = df.cache()
df_cached.count()  # Triggers caching

# Persist (Stored in Memory & Disk)
df_persisted = df.persist(StorageLevel.MEMORY_AND_DISK)
df_persisted.count()  # Triggers persistence
```
Key Takeaways:
1. Compare performance differences between cache & persist.
2. Use .persist(StorageLevel.DISK_ONLY) for large datasets.

## File Formats & Read Performance

Goal: Compare CSV vs Parquet performance.

Exercise 6: CSV vs Parquet Speed Test
```
import time

df = spark.range(1, 1000000).withColumnRenamed("id", "value")

# Write Data in CSV & Parquet
df.write.mode("overwrite").csv("/tmp/data_csv")
df.write.mode("overwrite").parquet("/tmp/data_parquet")

# Read CSV & Measure Time
start_time = time.time()
df_csv = spark.read.csv("/tmp/data_csv", inferSchema=True, header=True)
df_csv.count()
print("CSV Read Time:", time.time() - start_time)

# Read Parquet & Measure Time
start_time = time.time()
df_parquet = spark.read.parquet("/tmp/data_parquet")
df_parquet.count()
print("Parquet Read Time:", time.time() - start_time)
```
Key Takeaways:
1. Parquet is faster because of columnar storage.
2. CSV needs schema inference, slowing down reads.
