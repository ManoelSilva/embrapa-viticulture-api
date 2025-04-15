from service.extractor import EMBRAPAExtractorService
import pytest
from unittest.mock import patch, Mock
import pandas as pd
from flask import Flask


class TestEMBRAPAExtractorService(object):
    @pytest.fixture
    def app(self):
        """Fixture to create a Flask app instance for testing"""
        app = Flask(__name__)
        return app

    @pytest.fixture
    def extractor_service(self):
        """Fixture to create an instance of EMBRAPAExtractorService with mocked dependencies"""
        duck_db_mock = Mock()
        duck_db_mock.get_views.return_value = []
        return EMBRAPAExtractorService(duck_db_mock)

    @patch('service.extractor.EMBRAPAScrapperService.scrape_and_parse_tables')
    def test_extract_data_from_duckdb(self, mock_scrape, app, extractor_service):
        """
        Checks if data is retrieved from DuckDB when the view exists
        """
        data = [{'col1': 1, 'col2': 'a'}, {'col1': 2, 'col2': 'b'}]
        mock_df = pd.DataFrame(data)

        extractor_service._duck_db.get_views.return_value = ['processing_hybrid_americans']
        extractor_service._duck_db.fetch_data.return_value = mock_df

        with app.app_context():
            response = extractor_service.extract_data('processing', 'hybrid_americans')

            assert response.get_json() == data
            extractor_service._duck_db.get_views.assert_called_once()
            extractor_service._duck_db.fetch_data.assert_called_once_with('processing_hybrid_americans')
            mock_scrape.assert_not_called()

    @patch('service.extractor.EMBRAPAScrapperService.scrape_and_parse_tables')
    def test_extract_data_from_scrapper_when_view_not_exists(self, mock_scrape, app, extractor_service):
        """
        Checks if data is scraped and loaded when the view does not exist in DuckDB
        """
        data = [{'col1': 1, 'col2': 'a'}, {'col1': 2, 'col2': 'b'}]
        mock_df = pd.DataFrame(data)

        extractor_service._duck_db.get_views.return_value = []
        mock_scrape.return_value = mock_df

        with app.app_context():
            response = extractor_service.extract_data('processing', 'hybrid_americans')

            assert response.get_json() == data
            extractor_service._duck_db.get_views.assert_called_once()
            mock_scrape.assert_called_once_with(resource='processing', sub_resource='hybrid_americans', year=None)
            extractor_service._duck_db.create_dataframe_view.assert_called_once_with('processing_hybrid_americans',
                                                                                     mock_df)

    @patch('service.extractor.EMBRAPAScrapperService.scrape_and_parse_tables')
    def test_extract_data_from_scrapper_when_duckdb_fails(self, mock_scrape, app, extractor_service):
        """
        Checks if data is scraped and loaded when DuckDB fetch fails
        """
        data = [{'col1': 1, 'col2': 'a'}, {'col1': 2, 'col2': 'b'}]
        mock_df = pd.DataFrame(data)

        extractor_service._duck_db.get_views.return_value = ['processing_hybrid_americans']
        extractor_service._duck_db.fetch_data.return_value = None
        mock_scrape.return_value = mock_df

        with app.app_context():
            response = extractor_service.extract_data('processing', 'hybrid_americans')

            assert response.get_json() == data
            extractor_service._duck_db.get_views.assert_called_once()
            extractor_service._duck_db.fetch_data.assert_called_once_with('processing_hybrid_americans')
            mock_scrape.assert_called_once_with(resource='processing', sub_resource='hybrid_americans', year=None)
            extractor_service._duck_db.create_dataframe_view.assert_called_once_with('processing_hybrid_americans',
                                                                                     mock_df)
