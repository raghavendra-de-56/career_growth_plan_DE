Apache Spark is a distributed computing framework optimized for big data processing. Understanding its internals helps in performance tuning, debugging, and architectural decisions

## Spark Architecture Overview

### Spark Components

1. Driver Program:
  The main entry point for Spark applications.
  
  It submits jobs, distributes tasks, and monitors execution.

2. Cluster Manager:

  Manages resource allocation (CPU, memory) across worker nodes.
  
  Can be YARN, Kubernetes, Mesos, or Standalone.

3. Executor:

  Runs on worker nodes and executes tasks.
  
  Each executor has its own memory and caches data locally.

4. Task:

  A unit of execution sent to an executor.
  
  Multiple tasks form a stage, and multiple stages form a job.

5. RDD (Resilient Distributed Dataset):

  Spark’s fundamental immutable distributed data structure.
  
  Supports transformations (map, filter) and actions (count, collect).

### Architecture Flow:

  1. Driver creates an RDD and triggers an action.
  
  
  2. SparkContext translates this into a DAG (Directed Acyclic Graph).
  
  
  3. DAG Scheduler breaks the DAG into stages.
  
  
  4. Task Scheduler assigns tasks to executors.
  
  
  5. Executors execute tasks in parallel and store intermediate data.
  
  
  6. Final output is sent back to the driver.

### Spark Execution Flow

🔹 DAG (Directed Acyclic Graph)

Spark lazily evaluates transformations and builds a DAG before execution.

DAG helps optimize execution by reordering operations and reducing shuffles.


🔹 Example DAG for a Spark Job

df = spark.read.csv("data.csv")  # Stage 1: Read data
df = df.filter(df["col1"] > 100)  # Stage 2: Filter transformation (lazy)
df = df.groupBy("col2").count()  # Stage 3: GroupBy (causes shuffle)
df.show()  # Action triggers execution

🔹 DAG Optimization

1. Stage Splitting: Divides DAG into narrow and wide transformations.


2. Pipeline Execution: Executes multiple operations in a single stage.


3. Shuffle Optimization: Reduces expensive data movement between nodes.

