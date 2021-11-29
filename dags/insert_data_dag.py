import airflow.utils.dates
from airflow import DAG
from airflow.hooks.base_hook import BaseHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator

from custom_modules.dag_github_to_postgres import GitHubToPostgresTransfer

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

    trigger_postgres_export = TriggerDagRunOperator(
        task_id='trigger_postgres_export',
        external_dag_id='export_postgres_to_s3'
    )

    trigger_spark_submit = TriggerDagRunOperator(
        task_id='trigger_spark_submit',
        external_dag_id='spark_submit_airflow'
    )

create_user_purchase_table >> populate_user_purchase_table >> [trigger_postgres_export, trigger_spark_submit]
