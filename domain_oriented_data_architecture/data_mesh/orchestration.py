# Airflow DAG to Orchestrate Data Product Pipelines
# In a real-world Data Mesh setup:
# Each domain (e.g., Retail, Marketing) has its own pipelines.
# Pipelines should be scheduled, monitored, and retried automatically.
# Orchestration tool like Airflow manages data freshness and SLAs.
# Airflow DAG Example: Retail Domain Product Pipeline

from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'retail_team',
    'depends_on_past': False,
    'email': ['alerts@datamesh-retail.com'],
    'email_on_failure': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'retail_orders_data_product_pipeline',
    default_args=default_args,
    description='Retail Orders Data Product ETL Pipeline',
    schedule_interval='@daily',
    start_date=days_ago(1),
    tags=['data-mesh', 'retail'],
) as dag:

    run_databricks_job = DatabricksSubmitRunOperator(
        task_id='run_orders_pipeline',
        existing_cluster_id='<your-cluster-id>',
        notebook_task={
            'notebook_path': '/Repos/retail_team/orders_data_pipeline',
        },
    )

    run_databricks_job


# What This DAG Does:
# Triggers Databricks Notebook daily
# Handles retries on failure
# Sends email alerts on error
# Can monitor SLAs easily via Airflow
