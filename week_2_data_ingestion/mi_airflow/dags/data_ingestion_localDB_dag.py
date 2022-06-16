from os import environ
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from ingestions_script import ingest_callable
local_workflow = DAG(
    dag_id="data_ingestion_localDB_dag",
    schedule_interval="0 6 2 * *",
    catchup=False,
    max_active_runs=1,
    start_date=datetime(2021,1,1),
)

# dataset_url = "https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_2022-01.parquet"
# dataset_file = "yellow_tripdata_2022-01"

path_to_local_home = environ.get("AIRFLOW_HOME", "/opt/airflow/")
URL_PREFIX= "https://nyc-tlc.s3.amazonaws.com/trip+data/"
URL_TEMPLATE = URL_PREFIX + "yellow_tripdata_{{ '{}-{}'.format(start_date.year,start_date.month) }}.parquet"
OUTPUT_FILE_TEMPLATE = "output_tripdata_{{ '{}-{}'.format(start_date.year,start_date.month) }}.parquet"
TABLE_NAME_TEMPLATE = "trips_data_{{ '{}-{}!.format(start_date.year,start_date.month) }}"

PG_HOST = environ.get("PG_HOST", "pg_container")
PG_PORT = environ.get("PG_PORT", "5432")
PG_USER = environ.get("PG_USER", "root")
PG_PASSWORD = environ.get("PG_PASSWORD", "root")
PG_DATABASE = environ.get("PG_DATABASE", "ny_taxi")

with local_workflow:
    wget_task_local = BashOperator(
        task_id="wget_task_local",
        bash_command= f'curl -sSL {URL_TEMPLATE} > {path_to_local_home}/{OUTPUT_FILE_TEMPLATE} && head -n 10 {path_to_local_home}/{OUTPUT_FILE_TEMPLATE}',
    )
    # ls_them = BashOperator(
    #     task_id="ls_them",
    #     bash_command= f'ls -l {path_to_local_home}',
    # )

    ingesting_task = PythonOperator(
        task_id="ingesting_task",
        python_callable=ingest_callable,
        # (user, password, host, port, db, table_name, csv_file)
        op_kwargs=dict(
         user = PG_USER,
         password = PG_PASSWORD,
         host = PG_HOST,
         port = PG_PORT,
         db = PG_DATABASE,
         table_name = TABLE_NAME_TEMPLATE,
         csv_file = OUTPUT_FILE_TEMPLATE
         ),
    )


    wget_task_local >> ingesting_task


