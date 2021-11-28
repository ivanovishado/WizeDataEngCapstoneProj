import io
import psycopg2
import boto3

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.sensors.external_task_sensor import ExternalTaskSensor

resource = boto3.resource('s3')
conn = psycopg2.connect(
    dbname=Variable.get("USER_PURCHASE_DBNAME"),
    user=Variable.get("USER_PURCHASE_USER"),
    password=Variable.get("USER_PURCHASE_PASS"),
    host=Variable.get("USER_PURCHASE_HOST")
)
cur = conn.cursor()

def copyFun(bucket, select_query, filename):
    query = f"""COPY {select_query} TO STDIN \
            WITH (FORMAT csv, DELIMITER ',', QUOTE '"', HEADER TRUE)"""
    file = io.StringIO()
    cur.copy_expert(query, file)
    resource.Object(bucket, f'data/{filename}.csv').put(Body=file.getvalue())

default_args = {
    'owner': 'ivan.galaviz',
    'depends_on_past': False,
    'start_date': days_ago(1)
}

with DAG('export_postgres_to_s3', default_args = default_args, schedule_interval = '@once') as dag:
    wait_for_populate_table = ExternalTaskSensor(
        task_id='wait_for_populate_table',
        external_dag_id='dag_insert_data',
        external_task_id='dag_github_to_postgres',
        start_date=days_ago(1),
        timeout=3600,
    )

    export_data = PythonOperator(
        task_id='export_postgres_to_s3',
        python_callable=copyFun,
        op_kwargs={
            "bucket": Variable.get("STAGING_BUCKET"),
            "select_query": "user_purchase",
            "filename": "user_purchase",
        }
    )

wait_for_populate_table >> export_data
