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

