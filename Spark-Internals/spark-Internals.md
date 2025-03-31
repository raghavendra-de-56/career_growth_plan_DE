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

df = spark.read.csv("data.csv")  # Stage 1: Read data
df = df.filter(df["col1"] > 100)  # Stage 2: Filter transformation (lazy)
df = df.groupBy("col2").count()  # Stage 3: GroupBy (causes shuffle)
df.show()  # Action triggers execution

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

df = spark.read.parquet("data.parquet")

df_filtered = df.filter(df["col1"] > 100)

df_filtered.explain(True)  # Shows Optimized Execution Plan

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


### Spark Shuffling & Partitioning

#### What is Shuffling?

Shuffle happens when data moves across nodes, typically in:
1. GroupBy operations
2. Joins (except Broadcast joins)
3. Repartitioning

Shuffle can be expensive due to network & disk I/O.

#### How to Reduce Shuffle?

1. Use Broadcast Joins for Small Tables

from pyspark.sql.functions import broadcast
df_large.join(broadcast(df_small), "id")  # Avoids shuffle

2. Optimize Partitioning

df = df.repartition(10, "col1")  # Repartition based on a column

Broadcast Joins Optimization

1. Spark shuffles data for large joins, causing slowness.
2. Use broadcast() when joining a small lookup table to avoid shuffle.


🔹 Example: Optimized Join Using Broadcast

from pyspark.sql.functions import broadcast
df_large = spark.read.parquet("large_data.parquet")
df_small = spark.read.parquet("small_lookup.parquet")

df_optimized = df_large.join(broadcast(df_small), "id")  # Avoids shuffle

#### Spark Storage Levels (Cache & Persist)

Cache vs. Persist

.cache(): Stores DataFrame only in memory.

.persist(StorageLevel): Allows fine-grained control (MEMORY_AND_DISK, DISK_ONLY, etc.).

Example: Using Cache & Persist

df_cached = df.cache()
df_cached.count()  # Materializes cache

df_persisted = df.persist()
df_persisted.count()

 Storage Levels | Storage Level| Memory | Disk | Serialized | 
 
 |----------------------  |--------|------|------------| 
 
 | MEMORY_ONLY            | ✅     | ❌   | ❌         | 
 
 | MEMORY_AND_DISK        | ✅     | ✅   | ❌         | 
 
 | MEMORY_ONLY_SER        | ✅     | ❌   | ✅         | 
 
 | DISK_ONLY              | ❌     | ✅   | ✅         |

#### Spark File Formats & Optimization

Best File Formats for Spark

Convert CSV to Parquet

df.write.mode("overwrite").parquet("data.parquet")

#### Avoiding Performance Bottlenecks

Avoiding UDFs (User-Defined Functions)

UDFs slow down execution since they don’t benefit from Catalyst Optimizer.

Use Spark’s built-in functions instead of UDFs whenever possible.

Example: Avoid UDFs & Use Built-in Functions

from pyspark.sql.functions import length

Avoid slow UDFs

def text_length(text):

    return len(text)

df = df.withColumn("text_length", length(df["text"]))  # Optimized
