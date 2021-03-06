from airflow import DAG
import airflow.utils.dates
from airflow.contrib.operators.emr_create_job_flow_operator import (
    EmrCreateJobFlowOperator,
)
from airflow.contrib.operators.emr_add_steps_operator import EmrAddStepsOperator
from airflow.contrib.sensors.emr_step_sensor import EmrStepSensor
from airflow.contrib.operators.emr_terminate_job_flow_operator import (
    EmrTerminateJobFlowOperator,
)
from airflow.models import Variable

classification_s3_script = "scripts/random_text_classification.py"
user_behavior_s3_script = "scripts/user_behavior_metrics.py"
reviews_input_path = "data/movie_review.csv"
purchases_input_path = "data/user_purchase.csv"
classification_output_path = "data/reviews"
user_behavior_output_path = "data/behavior"
spark_bucket = Variable.get("SPARK_BUCKET")

# Spark gets the input and stores the output in S3,
# but HDFS should be preferred for output when performance is a concern

# These can be put inside a function for portability
SPARK_STEPS = [
    {
        "Name": "Classify movie reviews",
        "ActionOnFailure": "CANCEL_AND_WAIT",
        "HadoopJarStep": {
            "Jar": "command-runner.jar",
            "Args": [
                "spark-submit",
                "--deploy-mode",
                "client",  # Can be changed to cluster
                "s3://{{ params.SPARK_BUCKET }}/{{ params.classification_s3_script }}",
                "--input",
                "s3://{{ params.RAW_BUCKET }}/{{ params.reviews_input_path }}",
                "--output",
                "s3://{{ params.STAGING_BUCKET }}/{{ params.classification_output_path }}",
            ],
        },
    },
    {
        "Name": "Calculate user behavior metrics",
        "ActionOnFailure": "CANCEL_AND_WAIT",
        "HadoopJarStep": {
            "Jar": "command-runner.jar",
            "Args": [
                "spark-submit",
                "--deploy-mode",
                "client",
                "s3://{{ params.SPARK_BUCKET }}/{{ params.user_behavior_s3_script }}",
                "--reviews",
                "s3://{{ params.STAGING_BUCKET }}/{{ params.classification_output_path }}",
                "--purchases",
                "s3://{{ params.STAGING_BUCKET }}/{{ params.purchases_input_path }}",
                "--date",
                "{{ ts }}",
                "--output",
                "s3://{{ params.STAGING_BUCKET }}/{{ params.user_behavior_output_path }}",
            ],
        },
    },
]

# Could add a function
JOB_FLOW_OVERRIDES = {
    "Name": "Movie review classifier",
    "ReleaseLabel": "emr-6.4.0",
    "LogUri": f"s3://{spark_bucket}/logs/log.txt",
    "Applications": [{"Name": "Hadoop"}, {"Name": "Spark"}],
    "Configurations": [
        {
            "Classification": "spark-env",
            "Configurations": [
                {
                    "Classification": "export",
                    "Properties": {"PYSPARK_PYTHON": "/usr/bin/python3"},
                }
            ],
        }
    ],
    "Instances": {
        "Ec2SubnetId": Variable.get("SUBNET_ID"),
        "InstanceGroups": [
            {
                "Name": "Master node",
                "Market": "SPOT",  # Could be changed for ON-DEMAND for a more important project
                "InstanceRole": "MASTER",
                "InstanceType": "m4.xlarge",
                "InstanceCount": 1,
            },
            {
                "Name": "Core - 2",
                "Market": "SPOT",
                "InstanceRole": "CORE",
                "InstanceType": "m4.xlarge",
                "InstanceCount": 1,
            },
        ],
        "KeepJobFlowAliveWhenNoSteps": True,
        "TerminationProtected": False,
    },
    "JobFlowRole": "EMR_EC2_DefaultRole",
    "ServiceRole": "EMR_DefaultRole",
}

default_args = {
    "owner": "ivan.galaviz",
    "depends_on_past": False,
    "start_date": airflow.utils.dates.days_ago(1),
}

with DAG(
    "spark_submit_airflow",
    default_args=default_args,
    schedule_interval=None,
    max_active_runs=1,
) as dag:
    create_emr_cluster = EmrCreateJobFlowOperator(
        task_id="create_emr_cluster",
        job_flow_overrides=JOB_FLOW_OVERRIDES,
        aws_conn_id="aws_default",
        emr_conn_id="emr_default",
        region_name="us-east-2",  # Could go in a variable
    )

    # There should be a process per task
    step_adder = EmrAddStepsOperator(
        task_id="add_steps",
        job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value') }}",
        aws_conn_id="aws_default",
        steps=SPARK_STEPS,
        params={
            "SPARK_BUCKET": spark_bucket,
            "RAW_BUCKET": Variable.get("RAW_BUCKET"),
            "STAGING_BUCKET": Variable.get("STAGING_BUCKET"),
            "user_behavior_s3_script": user_behavior_s3_script,
            "classification_s3_script": classification_s3_script,
            "reviews_input_path": reviews_input_path,
            "classification_output_path": classification_output_path,
            "purchases_input_path": purchases_input_path,
            "user_behavior_output_path": user_behavior_output_path,
        },
    )

    last_step = len(SPARK_STEPS) - 1
    step_checker = EmrStepSensor(
        task_id="watch_step",
        job_flow_id="{{ task_instance.xcom_pull('create_emr_cluster', key='return_value') }}",
        step_id="{{ task_instance.xcom_pull(task_ids='add_steps', key='return_value')["
        + str(last_step)
        + "] }}",
        aws_conn_id="aws_default",
    )

    terminate_emr_cluster = EmrTerminateJobFlowOperator(
        task_id="terminate_emr_cluster",
        job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value') }}",
        aws_conn_id="aws_default",
    )

create_emr_cluster >> step_adder >> step_checker >> terminate_emr_cluster
