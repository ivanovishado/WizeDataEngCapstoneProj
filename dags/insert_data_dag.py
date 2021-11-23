from airflow.models.base import Base
import airflow.utils.dates
from airflow import DAG
from airflow.hooks.base_hook import BaseHook

from custom_modules.dag_github_to_postgres import GitHubToPostgresTransfer
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    'owner': 'ivan.galaviz',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(1)
}

with DAG('dag_insert_data', default_args = default_args, schedule_interval = '@once') as dag:
    create_user_purchase_table = PostgresOperator(
        task_id="create_user_purchase_table",
        sql="sql/user_purchase_schema.sql",
    )

    populate_user_purchase_table = GitHubToPostgresTransfer(
        task_id = 'dag_github_to_postgres',
        conn=BaseHook.get_connection('postgres_default').get_uri(),
        dag=dag
    )

create_user_purchase_table >> populate_user_purchase_table
