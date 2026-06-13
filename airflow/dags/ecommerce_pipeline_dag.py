from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta



PROJECT_DIR = '/home/thecollective/projects/ecommerce_pipeline'
VENV_ACTIVATE = f"{PROJECT_DIR}/venv/bin/activate"

default_args = {
    "owner": "airflow",
    "retries": 1,
}

with DAG(
    dag_id="ecommerce_pipeline",
    default_args=default_args,
    description="Ingest CSVs, transform with dbt",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["ecommerce", "dbt"],
) as dag:

    ingest_data = BashOperator(
        task_id="ingest_raw_data",
        bash_command=f"source {VENV_ACTIVATE} && cd {PROJECT_DIR} && python ingestion/load_raw.py",
    )

    run_dbt = BashOperator(
        task_id="run_dbt_models",
        bash_command=f"source {VENV_ACTIVATE} && cd {PROJECT_DIR}/dbt_project/ecommerce && dbt run",
    )

    ingest_data >> run_dbt