import pytest
import pandas as pd
from service.duck_db import DuckDBService


class TestDuckdbService(object):
    @pytest.fixture
    def duckdb_service(self):
        return DuckDBService()

    @pytest.fixture
    def sample_df(self):
        data = [{'col1': 1, 'col2': 'a'}, {'col1': 2, 'col2': 'b'}]
        return pd.DataFrame(data)

    def test_fetch_data_success(self, duckdb_service, sample_df):
        """
        Checks if data is correctly fetched when valid table name is provided
        """
        duckdb_service.create_dataframe_view('test_table', sample_df)

        result = duckdb_service.fetch_data('test_table')

        assert not result.empty
        assert len(result) == 2
        assert list(result.columns) == ['col1', 'col2']

    def test_fetch_data_nonexistent_table(self, duckdb_service):
        """
        Checks if None is returned when table doesn't exist
        """
        result = duckdb_service.fetch_data('nonexistent_table')
        assert result is None

    def test_create_table_success(self, duckdb_service, sample_df):
        """
        Checks if table is correctly created when valid parameters are provided
        """
        duckdb_service.create_dataframe_view('test_table', sample_df)

        assert 'test_table' in duckdb_service.get_views()
        result = duckdb_service.fetch_data('test_table')
        assert result.equals(sample_df)

    def test_create_table_duplicate(self, duckdb_service, sample_df):
        """
        Checks if table is not duplicated when created multiple times
        """
        duckdb_service.create_dataframe_view('test_table', sample_df)
        duckdb_service.create_dataframe_view('test_table', sample_df)

        tables = duckdb_service.get_views()
        assert tables.count('test_table') == 1

    def test_get_tables_empty(self, duckdb_service):
        """
        Checks if empty list is returned when no tables are created
        """
        result = duckdb_service.get_views()

        assert isinstance(result, list)
        assert len(result) == 0

    def test_create_table_exception(self, duckdb_service):
        """
        Checks if error is handled when DataFrame is invalid
        """
        invalid_df = None
        initial_tables = len(duckdb_service.get_views())

        duckdb_service.create_dataframe_view('test_table', invalid_df)

        assert len(duckdb_service.get_views()) == initial_tables
        assert 'test_table' not in duckdb_service.get_views()
