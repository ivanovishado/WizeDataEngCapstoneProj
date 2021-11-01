from datetime import datetime, timedelta
from airflow import models
from airflow.operators.bash_operator import BashOperator

yesterday = datetime.combine(
   datetime.today() - timedelta(1),
   datetime.min.time())

default_dag_args = {
    'start_date': yesterday,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'project_id': "sample_project"
}

with models.DAG(
    'Bash_operations',
    schedule_interval=timedelta(days=1),
    default_args=default_dag_args) as dag:


    t1 = BashOperator(
        task_id='Make_directory', bash_command='mkdir folder_name', dag=dag)


    t2 = BashOperator(
        task_id='delete_directory', bash_command='rm -rf folder_name', dag=dag)

    t1 >> t2   # This is how we set dependency among two tasks
