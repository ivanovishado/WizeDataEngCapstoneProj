# My Wizeline Data Engineering Bootcamp Capstone Project

This project's meant to be run in the cloud, but I'm aiming to provide a way to test it locally as well.

## Dependencies

- Airflow: Assuming you're using Python 3.9, the easiest way to install Airflow 2.2.0 locally is running this command:

    ```sh
    pip install 'apache-airflow==2.2.0' --constraint 'https://raw.githubusercontent.com/apache/airflow/constraints-2.2.0/constraints-3.9.txt'
    ```

## How to run Airflow locally

First, define the `AIRFLOW_HOME` env variable to wherever you installed it. Then, run:

```sh
airflow standalone
```

## Get cluster up and running

If this is your first time using AWS, make sure to check for presence of the `EMR_EC2_DefaultRole` and `EMR_DefaultRole` default role as shown below.

```sh
aws iam list-roles | grep 'EMR_DefaultRole\|EMR_EC2_DefaultRole'
# "RoleName": "EMR_DefaultRole",
# "RoleName": "EMR_EC2_DefaultRole",
```

If the roles not present, create them using the following command:

```sh
aws emr create-default-roles
```

### Terraform

**Note**: Before anything else, please create the `.env` file in the same location as the `.env.sample` file, following its contents.

1. Move to `terraform` directory.
1. `terraform init`
1. `terraform plan`
1. `terraform apply --var-file=terraform.tfvars` if there were no errors with plan.

### Kubernetes & Helm

Run the following commands:

```sh
aws eks --region $(terraform output -raw region) update-kubeconfig --name $(terraform output -raw cluster_name)

export NFS_SERVER=$(terraform output -raw efs)

kubectl create namespace storage

helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/

helm install nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
    --namespace storage \
    --set nfs.server=$NFS_SERVER \
    --set nfs.path=/

kubectl create namespace airflow

helm repo add apache-airflow https://airflow.apache.org
```

### Installing Airflow on Kubernetes

1. Create `override.yaml` at the project's root.
1. Insert the variables that are missing based on the `override.yaml.example` file.
1. Run `helm install airflow -f ../airflow-values.yaml -f ../override.yaml apache-airflow/airflow --namespace airflow`

Just make sure that everything's up and running with `kubectl get pods -n airflow` and you're done!

After that, you can access the webserver with `kubectl port-forward svc/airflow-webserver 8080:8080 --namespace airflow`

### Considerations while testing on the local environment

Use this URL to connect to the PostgreSQL instance: `postgresql://ivan.galaviz@host.docker.internal:5432/awesome_db`

## Complications during development

- Knowing how and where to start with Terraform
  - Resources were great, but it was a challenge to understand everything that was in the provided examples to know how to use it appropriately.
- Needing to change the Terraform version I was using. (Solved with `tfswitch`)
- Resources don't appear to be deleted when running `terraform destroy`
- Switched to EKS because of the following reasons:
  - The other TF approaches didn't work.
  - Resources were not being deleted in their entirety with the other approaches.
- I had to use a hardcoded bucket name to be able to re-upload resources consistently after destroying the services in AWS.
- Still can't found a way to ignore uploading certain files to Airflow (`*.csv`, `*.md`, etc.)
- The outputs for the S3 resources can be optimized somehow.
- The files in S3 should be compressed.

## TODOs

- Remember to try https://diagrams.mingrammer.com/!
- Do the transformations in the EMR cluster, not in Redshift
- Read Postgres directly from Airflow to send data to S3, without using Spark
- Send the output of Spark jobs to S3 as .parquet files
- Search airflow operator from S3 to Redshift
- Make sure that Redshift's in the same VPC as everything else
- Remember to send inser_date from Airflow
