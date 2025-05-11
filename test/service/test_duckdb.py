import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.service.duck_db import DuckDBService


class TestDuckdbService(object):
    @pytest.fixture
    def mock_connection(self):
        mock_con = MagicMock()
        # Mock the initial SHOW TABLES call
        mock_con.execute.return_value.fetchdf.return_value = pd.DataFrame({'name': []})
        return mock_con

    @pytest.fixture
    def duckdb_service(self, mock_connection):
        with patch('src.service.duck_db.duckdb.connect', return_value=mock_connection):
            with patch('src.service.duck_db.os.environ', {'MOTHERDUCK_TOKEN': 'fake_token'}):
                service = DuckDBService()
                service._con = mock_connection
                service._duckdb_tables = []
                return service

    @pytest.fixture
    def sample_df(self):
        data = [{'col1': 1, 'col2': 'a'}, {'col1': 2, 'col2': 'b'}]
        return pd.DataFrame(data)

    def test_fetch_data_success(self, duckdb_service, sample_df, mock_connection):
        """
        Checks if data is correctly fetched when valid table name is provided
        """
        mock_connection.execute.return_value.fetchdf.return_value = sample_df
        duckdb_service._duckdb_tables = ['test_table']

        result = duckdb_service.fetch_data('test_table')

        assert not result.empty
        assert len(result) == 2
        assert list(result.columns) == ['col1', 'col2']
        mock_connection.execute.assert_called_with('SELECT * FROM test_table')

    def test_fetch_data_nonexistent_table(self, duckdb_service, mock_connection):
        """
        Checks if empty DataFrame is returned when table doesn't exist
        """
        mock_connection.execute.side_effect = Exception('Table not found')
        result = duckdb_service.fetch_data('nonexistent_table')
        assert isinstance(result, pd.DataFrame)
        assert result.empty

    def test_create_table_success(self, duckdb_service, sample_df, mock_connection):
        """
        Checks if table is correctly created when valid parameters are provided
        """
        # Reset mock to clear previous calls
        mock_connection.reset_mock()

        duckdb_service.create_dataframe_table('test_table', sample_df)

        assert 'test_table' in duckdb_service._duckdb_tables

        # Verify the sequence of calls
        calls = mock_connection.execute.call_args_list
        create_table_call = next(call for call in calls if 'CREATE OR REPLACE TABLE' in str(call))
        update_datetime_call = next(call for call in calls if 'UPDATE db_datetime' in str(call))

        assert create_table_call is not None
        assert update_datetime_call is not None

    def test_create_table_duplicate(self, duckdb_service, sample_df, mock_connection):
        """
        Checks if table is not duplicated when created multiple times
        """
        # Reset mock to clear previous calls
        mock_connection.reset_mock()

        # Set up initial state
        duckdb_service._duckdb_tables = ['test_table']

        # First call should not create table since it already exists
        duckdb_service.create_dataframe_table('test_table', sample_df)

        # Verify table was not added again
        assert duckdb_service._duckdb_tables.count('test_table') == 1

        # Verify no SQL calls were made since table already exists
        mock_connection.execute.assert_not_called()

    def test_get_tables_empty(self, duckdb_service):
        """
        Checks if empty list is returned when no tables are created
        """
        duckdb_service._duckdb_tables = []
        result = duckdb_service.get_tables()

        assert isinstance(result, list)
        assert len(result) == 0

    def test_create_table_exception(self, duckdb_service, mock_connection):
        """
        Checks if error is handled when DataFrame is invalid
        """
        # Reset mock to clear previous calls
        mock_connection.reset_mock()

        invalid_df = None
        initial_tables = len(duckdb_service._duckdb_tables)
        mock_connection.execute.side_effect = Exception('Invalid DataFrame')

        duckdb_service.create_dataframe_table('test_table', invalid_df)

        assert len(duckdb_service._duckdb_tables) == initial_tables
        assert 'test_table' not in duckdb_service._duckdb_tables
