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

## Complications during development

- Knowing how and where to start with Terraform
  - Resources were great, but it was a challenge to understand everything that was in the provided examples to know how to use it appropriately.
- Needing to change the Terraform version I was using. (Solved with `tfswitch`)
- Resources don't appear to be deleted when running `terraform destroy`

## Notes

Should add Docker to test locally (make sure that the major versions match)

Remember to try https://diagrams.mingrammer.com/!
