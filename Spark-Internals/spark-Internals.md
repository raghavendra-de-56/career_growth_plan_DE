Apache Spark is a distributed computing framework optimized for big data processing. Understanding its internals helps in performance tuning, debugging, and architectural decisions

1️⃣ Spark Architecture Overview

🔹 Spark Components

1. Driver Program:
The main entry point for Spark applications.

It submits jobs, distributes tasks, and monitors execution.

2. Cluster Manager:

Manages resource allocation (CPU, memory) across worker nodes.

Can be YARN, Kubernetes, Mesos, or Standalone.
