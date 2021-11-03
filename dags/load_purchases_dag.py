from airflow import DAG
from airflow.models import Variable

from custom_modules.dag_github_to_postgres import GitHubToPostgresTransfer

default_args = {
    'owner': 'ivan.galaviz',
    'depends_on_past': False
}

dag = DAG('dag_insert_data', default_args = default_args, schedule_interval = '@once')

process_dag = GitHubToPostgresTransfer(
    username=Variable.get("AIRFLOW_RDS_USER"),
    password=Variable.get("AIRFLOW_RDS_PASS"),
    endpoint=Variable.get("AIRFLOW_RDS_ENDPOINT"),
)

process_dag
