import airflow.utils.dates
from airflow import DAG
from airflow.hooks.base_hook import BaseHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator

from custom_modules.dag_github_to_postgres import GitHubToPostgresOperator

default_args = {
    "owner": "ivan.galaviz",
    "depends_on_past": False,
    "start_date": airflow.utils.dates.days_ago(1),
}

with DAG(
    "dag_insert_data", default_args=default_args, schedule_interval="@once"
) as dag:
    create_user_purchase_table = PostgresOperator(
        task_id="create_user_purchase_table",
        sql="sql/user_purchase_schema.sql",
    )

    populate_user_purchase_table = GitHubToPostgresOperator(
        task_id="dag_github_to_postgres",
        conn=BaseHook.get_connection("postgres_default").get_uri(),
    )

    trigger_postgres_export = TriggerDagRunOperator(
        task_id="trigger_postgres_export", trigger_dag_id="export_postgres_to_s3"
    )

    trigger_spark_submit = TriggerDagRunOperator(
        task_id="trigger_spark_submit", trigger_dag_id="spark_submit_airflow"
    )

# Ideally, the DAGs should not trigger others
# An idea would be to create a dummy file to see if the DAG was completed successfully

(
    create_user_purchase_table
    >> populate_user_purchase_table
    >> [trigger_postgres_export, trigger_spark_submit]
)
