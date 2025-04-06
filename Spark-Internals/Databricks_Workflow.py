# Databricks Workflow - Example JSON for Orchestration (notebook-based)
# Save this as job_workflow.json if using the Jobs API
workflow_json = {
  "name": "Week2-ETL-Workflow",
  "tasks": [
    {
      "task_key": "load_orders",
      "notebook_task": {
        "notebook_path": "/Repos/load_orders"
      },
      "new_cluster": {
        "spark_version": "12.2.x-scala2.12",
        "node_type_id": "i3.xlarge",
        "num_workers": 2
      }
    },
    {
      "task_key": "merge_updates",
      "depends_on": [{"task_key": "load_orders"}],
      "notebook_task": {
        "notebook_path": "/Repos/merge_order_updates"
      },
      "new_cluster": {
        "spark_version": "12.2.x-scala2.12",
        "node_type_id": "i3.xlarge",
        "num_workers": 2
      }
    }
  ]
}
