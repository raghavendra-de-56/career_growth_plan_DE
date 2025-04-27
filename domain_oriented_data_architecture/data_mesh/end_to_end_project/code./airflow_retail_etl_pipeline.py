# Airflow Orchestration Setup

# Airflow will schedule and orchestrate the following steps:

# 1. Ingest data from S3 (Bronze)
# 2. Transform and validate (Silver)
# 3. Aggregate facts (Gold)
# 4. Refresh Unity Catalog tables
# 5. Send Slack/email alert if anything fails

# Airflow DAG - Code Example

# airflow/dags/retail_etl_pipeline.py

from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator
from airflow.operators.email import EmailOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'staff_data_engineer',
    'depends_on_past': False,
    'email_on_failure': True,
    'email': ['alerts@yourcompany.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='retail_data_pipeline_dag',
    default_args=default_args,
    description='Retail ETL pipeline from Bronze to Gold',
    schedule_interval='0 * * * *', # Every hour
    start_date=days_ago(1),
    tags=['retail', 'databricks', 'unity_catalog'],
) as dag:

    ingest_bronze = DatabricksSubmitRunOperator(
        task_id='ingest_bronze_orders',
        databricks_conn_id='databricks_default',
        notebook_task={
            'notebook_path': '/Repos/your_email/retail/bronze_ingestion',
        },
    )

    transform_silver = DatabricksSubmitRunOperator(
        task_id='transform_silver_orders',
        databricks_conn_id='databricks_default',
        notebook_task={
            'notebook_path': '/Repos/your_email/retail/silver_transformation',
        },
    )

    load_gold = DatabricksSubmitRunOperator(
        task_id='load_gold_facts',
        databricks_conn_id='databricks_default',
        notebook_task={
            'notebook_path': '/Repos/your_email/retail/gold_aggregation',
        },
    )

    send_success_email = EmailOperator(
        task_id='send_success_email',
        to='data_team@yourcompany.com',
        subject='Retail Data Pipeline Success',
        html_content='The retail data pipeline ran successfully!',
    )

    ingest_bronze >> transform_silver >> load_gold >> send_success_email
