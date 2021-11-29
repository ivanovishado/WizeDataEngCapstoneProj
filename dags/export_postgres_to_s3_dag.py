import io
import psycopg2
import boto3

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.hooks.base_hook import BaseHook
from urllib.parse import urlparse

postgres_uri = BaseHook.get_connection('postgres_default').get_uri()
parsed_url = urlparse(postgres_uri)
username = parsed_url.username
password = parsed_url.password
database = parsed_url.path[1:]
hostname = parsed_url.hostname

conn = psycopg2.connect(
    dbname=database,
    user=username,
    password=password,
    host=hostname
)
cur = conn.cursor()

resource = boto3.resource('s3')

def copyFun(bucket, table_name, s3_path):
    query = f"""COPY {table_name} TO STDIN \
            WITH (FORMAT csv, DELIMITER ',', QUOTE '"', HEADER TRUE)"""
    file = io.StringIO()
    cur.copy_expert(query, file)
    resource.Object(bucket, s3_path).put(Body=file.getvalue())

default_args = {
    'owner': 'ivan.galaviz',
    'depends_on_past': False,
    'start_date': days_ago(1)
}

with DAG('export_postgres_to_s3', default_args = default_args, schedule_interval = None) as dag:
    export_data = PythonOperator(
        task_id='export_postgres_to_s3',
        python_callable=copyFun,
        op_kwargs={
            "bucket": Variable.get("STAGING_BUCKET"),
            "table_name": "user_purchase",
            "s3_path": "data/user_purchase.csv",
        }
    )

export_data
