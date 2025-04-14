import duckdb
from loguru import logger
from pandas import DataFrame


class DuckDBService(object):
    def __init__(self):
        self._con = duckdb.connect()
        self._duckdb_views = []
        self._user_column_definitions = {
            "id": "INTEGER",
            "username": "VARCHAR",
            "password": "VARCHAR",
            "created_at": "TIMESTAMP"
        }
        self._create_user_table()

    def fetch_data(self, table_name: str) -> DataFrame | None:
        try:
            logger.info(f'Fetching data {table_name} from duckdb')
            return self._con.execute(f'SELECT * FROM {table_name}').fetchdf()
        except Exception as e:
            logger.error(f'Error fetching table {table_name} from duckdb {e}')
            return None

    def create_dataframe_view(self, view_name: str, data_frame: DataFrame) -> None:
        try:
            if view_name not in self._duckdb_views:
                logger.info(f'Creating view {view_name} in duckdb')
                self._con.register(f'{view_name}', data_frame)
                self._duckdb_views.append(view_name)
        except Exception as e:
            logger.error(f'Error creating view {view_name} in duckdb {e}')

    def get_views(self) -> list[str]:
        return self._duckdb_views

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
            columns_definition = ", ".join([f"{col} {dtype}" for col, dtype in self._user_column_definitions.items()])
            create_user_table_query = f'CREATE TABLE users ({columns_definition})'
            self._con.execute(create_user_table_query)
            logger.info(f'Table users created successfully with columns: {self._user_column_definitions}')
        except Exception as e:
            logger.error(f'Error creating table users: {e}')
