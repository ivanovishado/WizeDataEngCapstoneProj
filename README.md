# My Wizeline Data Engineering Bootcamp Capstone Project

This is my Capstone project which implements a basic pipeline to **extract**, **transform**, and **load** user purchases and movie reviews.

## Dependencies

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Helm](https://helm.sh/docs/intro/install/)
- [Terraform](https://www.terraform.io/downloads.html)
- [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)

Configure the `AWS CLI` with your credentials by running `aws configure`.

### Local development

- [OpenJDK](https://openjdk.java.net/install/)
- [Apache Spark](https://formulae.brew.sh/formula/apache-spark)
- [parquet-tools](https://formulae.brew.sh/formula/parquet-tools)
- [jenv](https://www.jenv.be/)
- I strongly recommend taking a look to [Airflow Breeze](https://github.com/apache/airflow/blob/main/BREEZE.rst) to execute Airflow in your local environment.
- There are several ways to install Postgres locally, but I recommend [Postgres.app](https://postgresapp.com/) and [Postico](https://eggerapps.at/postico/) to query it.
- Then, you can install everything else by running `pip install -r dev-requirements.txt`. Preferably in a virtual environment.

## Get cluster up and running

### Pre-steps

If this is your first time using AWS, make sure to check for presence of the `EMR_EC2_DefaultRole` and `EMR_DefaultRole` default role as shown below.

```sh
aws iam list-roles | grep 'EMR_DefaultRole\|EMR_EC2_DefaultRole'
# "RoleName": "EMR_DefaultRole",
# "RoleName": "EMR_EC2_DefaultRole",
```

If the roles are not present, create them using the following command:

```sh
aws emr create-default-roles
```

### Terraform

**Note**: Please create the `terraform/.env` file in the same location as the `terraform/.env.sample` file, following its contents.

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

Then, run

```sh
make upload_files_to_s3
```

To upload the neccessary files to S3.

### Installing Airflow on Kubernetes

1. Create `override.yaml` at the project's root.
1. Insert the variables that are missing based on the `override.yaml.example` file.
1. Run `helm install airflow -f ../airflow-values.yaml -f ../override.yaml apache-airflow/airflow --namespace airflow`

Just make sure that everything's up and running with `kubectl get pods -n airflow` and you're done!

After that, you can access the webserver with `kubectl port-forward svc/airflow-webserver 8080:8080 --namespace airflow`

### Considerations while testing on the local environment

- `host.docker.internal` DNS address will resolve to the host's actual address when running inside Docker.

## Complications during development

- Knowing how and where to start with Terraform
  - Resources were great, but it was a challenge to understand everything that was in the provided examples to know how to use it appropriately.
- Needing to change the Terraform version I was using. (Solved with `tfswitch`)
- Resources don't appear to be deleted when running `terraform destroy`
- Switched to EKS because of the following reasons:
  - The other TF approaches didn't work.
  - Resources were not being deleted in their entirety with the other approaches.
- Still can't find a way to ignore uploading certain files to Airflow (`*.csv`, `*.md`, etc.)
- The outputs for the S3 resources can be optimized somehow.
- The files in S3 should be compressed.

## TODOs

- Remember to try https://diagrams.mingrammer.com/!
- See if EMR hardware can be reduced
- Convert buckets to private
- Separate Spark steps in DAG
- Add `AmazonS3FullAccess` to `EMR_DefaultRole`
- Add scripts for manual steps
- Do the transformations in the EMR cluster, not in Redshift
- Read Postgres directly from Airflow to send data to S3, without using Spark
- Make sure that Redshift's in the same VPC as everything else
- Remember to send inser_date from Airflow
- Use HDFS in the Spark section
- Improve IAM access
- Ask if the index in user_purchase.csv is needed
