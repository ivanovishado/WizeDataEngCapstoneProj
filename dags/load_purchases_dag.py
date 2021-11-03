import airflow.utils.dates
from airflow import DAG
from airflow.models import Variable

from custom_modules.dag_github_to_postgres import GitHubToPostgresTransfer

default_args = {
    'owner': 'ivan.galaviz',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(1)
}

dag = DAG('dag_insert_data', default_args = default_args, schedule_interval = '@once')

process_dag = GitHubToPostgresTransfer(
    task_id = 'dag_github_to_postgres',
    username=Variable.get("AIRFLOW_RDS_USER"),
    password=Variable.get("AIRFLOW_RDS_PASS"),
    endpoint=Variable.get("AIRFLOW_RDS_ENDPOINT"),
    dag=dag
)

process_dag
