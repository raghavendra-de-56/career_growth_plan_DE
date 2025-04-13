## Orchestration (Data Pipeline Management)

### What It Is:
Orchestration is the coordination of automated tasks (ETL/ELT jobs, validations, alerts) across a data pipeline in a defined order, with error handling and retries.

### Key Tools:

1. Apache Airflow
2. Databricks Workflows
3. Dagster / Prefect (modern alternatives)

### Key Concepts:

1. DAG (Directed Acyclic Graph)
2. Scheduling & Dependencies
3. Retries and Failover
4. Notification/Alerting (Slack, email, etc.)
5. Parameterization & Environment config
6. Dynamic task generation

### Real-World Use Case (IoT Analytics):

1. Ingest raw IoT data (Kafka/S3 to Delta)
2. Run data quality checks
3. Transform & enrich data
4. Aggregate for reporting
5. Notify downstream systems (Slack/API trigger)

### Best Practices:

1. Use separate DAGs per domain or SLA-critical path
2. Add retries, SLAs, and alerts
3. Monitor orchestration logs centrally (e.g., Airflow logs via S3/Datadog)
4. Store orchestration state externally (e.g., Airflow metadata DB)

## DAG Design Principles

1. Ensure idempotency for re-runs.
2. Split pipelines by domain or SLA boundaries.
3. Use task-level retries and SLA monitoring.

```
# Example: Defining tasks with dependencies
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def extract():
    print("Extracting...")

def transform():
    print("Transforming...")

def load():
    print("Loading...")

dag = DAG('elt_pipeline', start_date=datetime(2023,1,1), schedule_interval='@daily')

t1 = PythonOperator(task_id='extract', python_callable=extract, dag=dag)
t2 = PythonOperator(task_id='transform', python_callable=transform, dag=dag)
t3 = PythonOperator(task_id='load', python_callable=load, dag=dag)

t1 >> t2 >> t3
```
## Orchestration using Databricks Workflows

```
# Create a job using Databricks CLI or API

# Sample task JSON for a multi-task job
{
  "name": "iot-ingestion-pipeline",
  "tasks": [
    {
      "task_key": "ingest_data",
      "notebook_task": {
        "notebook_path": "/Users/iot/ingest_data"
      },
      "cluster_spec": {
        "existing_cluster_id": "XXXX-XXXXXXX"
      }
    },
    {
      "task_key": "validate_schema",
      "notebook_task": {
        "notebook_path": "/Users/iot/validate_schema"
      },
      "depends_on": [
        { "task_key": "ingest_data" }
      ]
    }
  ]
}
```
## Airflow Monitoring and Alerting
```
# Sample alerting config using Slack webhook
from airflow.operators.email_operator import EmailOperator

alert = EmailOperator(
    task_id='email_alert',
    to='dataops@company.com',
    subject='Pipeline Failure',
    html_content='Check Airflow for failed DAG',
    dag=dag
)
```
## Retry Strategies and Recovery

```
from airflow.operators.python_operator import PythonOperator

# Retry up to 3 times with 5 min delay
task = PythonOperator(
    task_id='resilient_task',
    python_callable=my_function,
    retries=3,
    retry_delay=timedelta(minutes=5),
    dag=dag
)
```
