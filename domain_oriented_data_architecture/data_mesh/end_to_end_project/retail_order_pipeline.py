# Orchestration using Airflow DAG

# Airflow DAG: retail_order_pipeline.py

from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from datetime import datetime

default_args = {"start_date": datetime(2024, 1, 1)}

dag = DAG('retail_order_pipeline', default_args=default_args, schedule_interval='@daily', catchup=False)

ingest_task = DatabricksRunNowOperator(
    task_id='batch_ingestion',
    databricks_conn_id='databricks_default',
    job_id='YOUR_DATABRICKS_JOB_ID',
    dag=dag
)

validate_task = DatabricksRunNowOperator(
    task_id='data_quality_validation',
    databricks_conn_id='databricks_default',
    job_id='YOUR_DATABRICKS_JOB_ID',
    dag=dag
)

ingest_task >> validate_task
