
# Week 2: Interview Quiz & Cheat Sheet

## Quick Quiz (Self-Evaluation)

1. **What is data skew and how does it impact Spark jobs?**
   - *Follow-up:* What are two ways to mitigate skew in joins?

2. **Explain the difference between `merge` and `insert overwrite` in Delta Lake.**
   - *Which one is better for CDC (Change Data Capture) use cases?*

3. **What does OPTIMIZE and ZORDER BY do in Delta Lake?**
   - *When should you use them?*

4. **How does Delta Lake enable time travel? What’s the practical use case for it?**

5. **In your pipeline, how would you handle a failure during an upsert step?**

6. **Can you explain the role of broadcast join in Spark and when it's ideal to use it?**

7. **How would you structure an end-to-end batch pipeline to be idempotent?**

8. **What is a common mistake people make when dealing with large joins in Spark?**

9. **Why is salting considered a trade-off, and what could go wrong if overused?**

10. **What is the significance of schema evolution in Delta Lake pipelines?**

---

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
