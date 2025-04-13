## Orchestration (Data Pipeline Management)

### What is Orchestration in Data Engineering?

Orchestration refers to the automated coordination, scheduling, and monitoring of data pipelines and workflows — ensuring that each step of a process happens in the right sequence, handles errors gracefully, and integrates with infrastructure components effectively.

Think of orchestration as the conductor of a data symphony — directing when and how different parts of your data processing play out, across batch, streaming, and ML jobs.

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

## Designing resilient, observable, and scalable workflows

1. Integrating across data lakes, streaming systems, and external APIs
2. Owning cross-team data dependencies
3. Creating platform capabilities and standards for orchestration

## Key Orchestration Concepts

1. Directed Acyclic Graphs (DAGs)

Definition: A DAG represents tasks (nodes) and their dependencies (edges). It ensures no cycles — a task can't depend on itself.

Example: Extract → Transform → Load

2. Task Dependencies

You define relationships like:

Task B runs after Task A (A >> B)

Task C depends on Task A and B

3. Scheduling

Defines when the DAG runs (e.g., daily at midnight).

Also includes backfilling for historical data and triggering from events.

4. Idempotency

Ensures re-running a task doesn’t corrupt data.

Implemented by partitioned writes, upserts, or snapshotting.

5. Retries and Timeouts

Control resilience: retries with exponential backoff, task timeout kill logic.

Helps with flaky external systems (e.g., REST APIs).

6. Monitoring & Alerting

Use built-in UIs (Airflow, Databricks) and integrate with PagerDuty, Slack, etc.

Metrics to track: DAG duration, task retries, SLA misses, data freshness.

## Real-World Orchestration Examples

### 1. Daily Supply Chain Data Ingestion

1. Schedule every day at 2am
2. Task sequence:
3. Extract data from SAP (Task A)
4. Validate schema (Task B)
5. Transform into Delta Lake format (Task C)
6. Load into Snowflake for planning tools (Task D)
7. Airflow manages the job, with email alert if failure occurs.

## Best Practices

1. Design DAGs for Modularity: Reuse components across pipelines.
2. Standardize Retry & Alerting Logic: Use wrappers or decorators.
3. Abstract Pipeline Configuration: Use YAML/JSON to drive DAG generation.
4. Build Observability In: Emit metrics from all tasks.
5. Think in SLAs and Data Contracts: Ensure pipelines meet downstream expectations.
6. Platform Mindset: Enable others to build DAGs via templates, APIs, or UI forms.


### 2. IoT Stream + Batch Hybrid Pipeline

1. Kafka stream ingests sensor data (real-time)
2. Airflow runs hourly aggregation jobs
3. Databricks Workflow triggers ML model scoring every 6 hours on recent data
4. Alerts if missing >10% of sensor readings for the hour

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
