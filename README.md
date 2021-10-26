# My Wizeline Data Engineering Bootcamp Capstone Project

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
