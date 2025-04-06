
# Week 2: Interview Quiz & Cheat Sheet

## Quick Quiz (Self-Evaluation)

1. **What is data skew and how does it impact Spark jobs?**
   - *Follow-up:* What are two ways to mitigate skew in joins?

      Data skew occurs when some keys in a join or aggregation are significantly more frequent than others, leading to uneven partition sizes.
      Impact: Spark tasks processing skewed partitions take much longer, causing overall job slowdown or even failure due to out-of-memory errors.
      
      Mitigation Techniques:
      
      Salting: Add a random prefix or suffix to skewed keys to distribute them across partitions.
      
      Broadcast Join: Use when the other table is small enough (typically <100MB) to avoid shuffle.

2. **Explain the difference between `merge` and `insert overwrite` in Delta Lake.**
   - *Which one is better for CDC (Change Data Capture) use cases?*
  
      MERGE INTO allows conditional updates, inserts, and deletes in one atomic operation. It's ideal for CDC where you need to upsert based on changes.
      
      INSERT OVERWRITE replaces the entire data in a partition or table—less flexible for incremental updates.
      
      Better for CDC? → MERGE INTO is preferred due to fine-grained update capability.

3. **What does OPTIMIZE and ZORDER BY do in Delta Lake?**
   - *When should you use them?*
  
     OPTIMIZE compacts small files in Delta Lake tables into larger ones for better read performance.
      
      ZORDER BY reorders the data files based on column values to improve data skipping during filtering.
      
      Use when:
      
      Large tables with frequent queries on specific columns.
      
      After many small file writes (like from streaming).

4. **How does Delta Lake enable time travel? What’s the practical use case for it?**

      Delta maintains a transaction log (_delta_log) of every write.
      You can query previous versions using:
      
      df = spark.read.format("delta").option("versionAsOf", 5).load("/path")
      
      Use Case:
      
      Debugging or comparing data over time.
      
      Rollbacks or reproducing historical reports.

5. **In your pipeline, how would you handle a failure during an upsert step?**

      Implement retry logic in orchestration (e.g., Airflow retry).
      
      Log audit trail (success/failure) and support idempotency—design the MERGE such that re-running it won’t duplicate or corrupt data.
      
      Add alerting/monitoring to notify stakeholders.

6. **Can you explain the role of broadcast join in Spark and when it's ideal to use it?**

      Spark replicates the smaller dataset to all workers to avoid shuffle.
      Use when:
      
      One side of the join is significantly smaller (e.g., <100MB).
      
      You're joining a large fact table with a small dimension table.
      
      broadcast(df_small)

7. **How would you structure an end-to-end batch pipeline to be idempotent?**

      Use unique keys or composite keys to detect duplicates.
      
      Implement merge logic (instead of insert-only).
      
      Use checkpoints for intermediate states.
      
      Partitioning based on ingestion time or business key helps avoid reprocessing issues.

8. **What is a common mistake people make when dealing with large joins in Spark?**

      Not analyzing data size before choosing join strategy.
   
      Using default shuffle join without optimization.
      
      Forgetting to cache reused dataframes.
      
      Joining without pre-filtering unnecessary rows.

9. **Why is salting considered a trade-off, and what could go wrong if overused?**

      Pros: Solves data skew.
      
      Cons: Increases data duplication and post-processing complexity.
      If overused, salting can make downstream joins or groupings less efficient and harder to manage.

10. **What is the significance of schema evolution in Delta Lake pipelines?**

      Allows your tables to adapt to new columns without breaking production pipelines.
      Useful in:
      
      IoT or event-based systems with evolving structures.
      
      Supporting multiple source systems with slightly varying schemas.
      
      Enable it with:
      
      ```.option("mergeSchema", "true")```

## Cheat Sheet: Key Concepts

| Topic               | Summary                                                                 |
|--------------------|-------------------------------------------------------------------------|
| **Data Skew**       | Uneven distribution of keys in join operations; can be resolved with **salting** or **broadcast joins**. |
| **Salting**         | Adds random suffix to skewed keys to distribute load across partitions. |
| **Broadcast Join**  | Replicates smaller dataset to all executors; avoids shuffle-heavy operations. Ideal when one dataset is < 100MB. |
| **Delta Lake Merge**| Used for **upserts**. Maintains ACID transactions.                      |
| **ZORDER BY**       | Used after OPTIMIZE to cluster data by column for faster filtering.     |
| **Time Travel**     | Use `.option("versionAsOf", n)` or `.option("timestampAsOf", "...")` to query historical snapshots. |
| **OPTIMIZE**        | Compacts small files in Delta tables, improving read performance.        |
| **Orchestration**   | Use tools like Airflow or Databricks Workflows to chain and monitor pipeline steps. |
| **Schema Evolution**| Delta Lake supports `mergeSchema` and handles evolving schemas in production. |
| **Idempotency**     | Ensure pipelines can safely rerun without duplication or corruption.     |
