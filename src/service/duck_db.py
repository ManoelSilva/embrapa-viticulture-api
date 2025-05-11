import os

import duckdb
from loguru import logger
import pandas as pd
from pandas import DataFrame


class DuckDBService(object):
    _DB_DATETIME_ID = 0

    def __init__(self):
        token = os.environ.get('MOTHERDUCK_TOKEN')
        os.environ['DUCKDB_HOME'] = '/tmp'
        self._con = duckdb.connect(f'md:winemaking?motherduck_token={token}&home_directory=/tmp')
        self._duckdb_tables = self._con.execute("SHOW TABLES").fetchdf()['name'].tolist()
        self._user_column_definitions = {
            "id": "INTEGER",
            "username": "VARCHAR",
            "password": "VARCHAR",
            "created_at": "TIMESTAMP"
        }
        self._db_datetime_column_definitions = {
            "id": "INTEGER PRIMARY KEY",
            "datetime": "TIMESTAMP"
        }
        self._create_user_table()
        self._create_datetime_table()

    def fetch_data(self, table_name: str) -> DataFrame:
        try:
            logger.info(f'Fetching data {table_name} from duckdb')
            return self._con.execute(f'SELECT * FROM {table_name}').fetchdf()
        except Exception as e:
            logger.error(f'Error fetching table {table_name} from duckdb {e}')
            return pd.DataFrame()

    def create_dataframe_table(self, table_name: str, data_frame: DataFrame) -> None:
        try:
            if table_name not in self._duckdb_tables:
                logger.info(f'Creating table {table_name} in duckdb')
                self._con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM {data_frame}")
                self._con.execute(
                    f'UPDATE db_datetime SET datetime = CURRENT_TIMESTAMP WHERE id = {self._DB_DATETIME_ID}')
                self._duckdb_tables.append(table_name)
        except Exception as e:
            logger.error(f'Error creating table {table_name} in duckdb {e}')

    def get_tables(self) -> list[str]:
        return self._duckdb_tables

    def user_exists(self, username: str) -> bool:
        try:
            users = self.fetch_data('users')
            return users is not None and username in users['username'].values
        except Exception as e:
            logger.error(f'Error checking if user exists: {e}')
            return False

    def insert_user(self, username: str, hashed_password: str) -> None:
        try:
            self._con.execute(
                "INSERT INTO users (username, password, created_at) VALUES (?, ?, CURRENT_TIMESTAMP)",
                (username, hashed_password)
            )
            logger.info(f'User {username} inserted successfully')
        except Exception as e:
            logger.error(f'Error inserting user {username}: {e}')

    def _create_user_table(self) -> None:
        try:
            columns_definition = self._get_columns_definition(self._user_column_definitions)
            create_user_table_query = f'CREATE TABLE IF NOT EXISTS users ({columns_definition})'
            self._con.execute(create_user_table_query)
            logger.info(f'Table users created successfully with columns: {self._user_column_definitions}')
        except Exception as e:
            logger.error(f'Error creating table users: {e}')

    def _create_datetime_table(self) -> None:
        try:
            columns_definition = self._get_columns_definition(self._db_datetime_column_definitions)
            create_datetime_table_query = \
                f'CREATE TABLE IF NOT EXISTS db_datetime ({columns_definition})'
            self._con.execute(create_datetime_table_query)
            self._con.execute(
                f'INSERT INTO db_datetime (id, datetime) VALUES ({self._DB_DATETIME_ID}, CURRENT_TIMESTAMP) '
                f'ON CONFLICT (id) DO NOTHING'
            )
            logger.info(f'Table db_datetime created successfully with columns: {self._db_datetime_column_definitions}')
        except Exception as e:
            logger.error(f'Error creating table db_datetime: {e}')

    @staticmethod
    def _get_columns_definition(columns_dict: dict) -> str:
        return ", ".join([f"{col} {dtype}" for col, dtype in columns_dict.items()])
