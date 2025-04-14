from service.extractor import EMBRAPAExtractorService
import pytest
from unittest.mock import patch
import pandas as pd
from flask import Flask


class TestExtractorService(object):
    @pytest.fixture
    def app(self):
        app = Flask(__name__)
        return app

    @pytest.fixture
    def extractor_service(self):
        return EMBRAPAExtractorService()

    def test_extract_data_from_duckdb(self, app, extractor_service):
        """
        Checks if data is retrieved from DuckDB when table exists
        """
        data = [{'col1': 1, 'col2': 'a'}, {'col1': 2, 'col2': 'b'}]
        mock_df = pd.DataFrame(data)

        with app.app_context(), \
                patch.object(extractor_service._duck_db, 'get_tables', return_value=['import_grape_juice_2023']), \
                patch.object(extractor_service._duck_db, 'fetch_data', return_value=mock_df):
            response = extractor_service.extract_data('import', 'grape_juice', '2023')

            assert response.get_json() == data

    def test_extract_data_from_scrapper_when_table_not_exists(self, app, extractor_service):
        """
        Checks if data is scraped when table does not exist in DuckDB
        """
        data = [{'col1': 1, 'col2': 'a'}, {'col1': 2, 'col2': 'b'}]
        mock_df = pd.DataFrame(data)

        with app.app_context(), \
                patch.object(extractor_service._duck_db, 'get_tables', return_value=[]), \
                patch.object(extractor_service._scrapper, 'scrape_and_parse_tables', return_value=mock_df), \
                patch.object(extractor_service._duck_db, 'create_table') as mock_create:
            response = extractor_service.extract_data('import', 'grape_juice', '2023')

            assert response.get_json() == data
            mock_create.assert_called_once_with('import_grape_juice_2023', mock_df)

    def test_extract_data_from_scrapper_when_duckdb_fails(self, app, extractor_service):
        """
        Checks if data is scraped when DuckDB fetch fails
        """
        data = [{'col1': 1, 'col2': 'a'}, {'col1': 2, 'col2': 'b'}]
        mock_df = pd.DataFrame(data)

        with app.app_context(), \
                patch.object(extractor_service._duck_db, 'get_tables', return_value=['import_grape_juice_2023']), \
                patch.object(extractor_service._duck_db, 'fetch_data', return_value=None), \
                patch.object(extractor_service._scrapper, 'scrape_and_parse_tables', return_value=mock_df), \
                patch.object(extractor_service._duck_db, 'create_table') as mock_create:
            response = extractor_service.extract_data('import', 'grape_juice', '2023')

            assert response.get_json() == data
            mock_create.assert_called_once_with('import_grape_juice_2023', mock_df)
