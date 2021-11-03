from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import pandas as pd

import csv
from io import StringIO

from sqlalchemy import create_engine


class GitHubToPostgresTransfer(BaseOperator):
    """GitHubToPostgresTransfer: custom operator created to move small csv files of data
                             to a postgresDB, it was created for the bootcamp project.
       Author: Ivan Galaviz.

    Attributes:
    """

    @apply_defaults
    def __init__(
            self,
            username,
            password,
            endpoint,
            *args, **kwargs):
        super(GitHubToPostgresTransfer, self).__init__(*args, **kwargs)
        self.username = username
        self.password = password
        self.endpoint = endpoint

    def execute(self, context):
        df = pd.read_csv("https://raw.githubusercontent.com/ivanovishado/WizeDataEngCapstoneProj/main/user_purchase.csv")

        engine = create_engine(f'postgresql://{self.username}:{self.password}@{self.endpoint}/user_purchase')
        df.to_sql('user_purchase', engine, method=self.psql_insert_copy)

    def psql_insert_copy(self, table, conn, keys, data_iter):
        dbapi_conn = conn.connection
        with dbapi_conn.cursor() as cur:
            s_buf = StringIO()
            writer = csv.writer(s_buf)
            writer.writerows(data_iter)
            s_buf.seek(0)

            columns = ', '.join('"{}"'.format(k) for k in keys)
            if table.schema:
                table_name = '{}.{}'.format(table.schema, table.name)
            else:
                table_name = table.name

            sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(
                table_name, columns)
            cur.copy_expert(sql=sql, file=s_buf)
