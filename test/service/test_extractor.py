from unittest.mock import patch, Mock

import pandas as pd
import pytest
from flask import Flask
from pydantic import ValidationError

from src.service.extractor import EMBRAPAExtractorService


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
        duck_db_mock.get_tables.return_value = []
        duck_db_mock.fetch_data.return_value = pd.DataFrame({'datetime': [pd.Timestamp.now()]})
        return EMBRAPAExtractorService(duck_db_mock)

    @patch('src.service.extractor.EMBRAPAScrapperService.scrape_and_parse_tables')
    def test_extract_data_from_duckdb(self, mock_scrape, app, extractor_service):
        """
        Checks if data is retrieved from DuckDB when the view exists
        """
        data = [{'col1': 1, 'col2': 'a'}, {'col1': 2, 'col2': 'b'}]
        mock_df = pd.DataFrame(data)
        datetime_df = pd.DataFrame({'datetime': [pd.Timestamp.now()]})

        extractor_service._duck_db.get_tables.return_value = ['processing_hybrid_americans']
        extractor_service._duck_db.fetch_data.side_effect = [mock_df, datetime_df]

        with app.app_context():
            response = extractor_service.extract_data('processing', 'hybrid_americans')

            assert response.get_json() == data
            assert extractor_service._duck_db.get_tables.call_count == 1
            assert extractor_service._duck_db.fetch_data.call_count == 2
            mock_scrape.assert_not_called()

    @patch('src.service.extractor.EMBRAPAScrapperService.scrape_and_parse_tables')
    def test_extract_data_from_scrapper_when_view_not_exists(self, mock_scrape, app, extractor_service):
        """
        Checks if data is scraped and loaded when the view does not exist in DuckDB
        """
        data = [{'col1': 1, 'col2': 'a'}, {'col1': 2, 'col2': 'b'}]
        mock_df = pd.DataFrame(data)
        datetime_df = pd.DataFrame({'datetime': [pd.Timestamp.now()]})

        extractor_service._duck_db.get_tables.return_value = []
        mock_scrape.return_value = mock_df
        extractor_service._duck_db.fetch_data.return_value = datetime_df

        with app.app_context():
            response = extractor_service.extract_data('processing', 'hybrid_americans')

            assert response.get_json() == data
            assert extractor_service._duck_db.get_tables.call_count == 1
            mock_scrape.assert_called_once_with(resource='processing', sub_resource='hybrid_americans', year=None)
            extractor_service._duck_db.create_dataframe_table.assert_called_once_with('processing_hybrid_americans',
                                                                                      mock_df)

    @patch('src.service.extractor.EMBRAPAScrapperService.scrape_and_parse_tables')
    def test_extract_data_from_scrapper_when_duckdb_fails(self, mock_scrape, app, extractor_service):
        """
        Checks if data is scraped and loaded when DuckDB fetch fails
        """
        data = [{'col1': 1, 'col2': 'a'}, {'col1': 2, 'col2': 'b'}]
        mock_df = pd.DataFrame(data)

        extractor_service._duck_db.get_tables.return_value = ['processing_hybrid_americans']
        extractor_service._duck_db.fetch_data.return_value = None
        mock_scrape.return_value = mock_df

        with app.app_context():
            response = extractor_service.extract_data('processing', 'hybrid_americans')

            assert response.get_json() == data
            assert extractor_service._duck_db.get_tables.call_count == 1
            assert extractor_service._duck_db.fetch_data.call_count == 1
            mock_scrape.assert_called_once_with(resource='processing', sub_resource='hybrid_americans', year=None)
            extractor_service._duck_db.create_dataframe_table.assert_called_once_with('processing_hybrid_americans',
                                                                                      mock_df)

    def test_get_validated_year(self, extractor_service):
        """
        Tests the _get_validated_year method with different year inputs
        """
        # Test with valid year
        assert extractor_service._get_validated_year(2023) == "2023"

        # Test with None year
        assert extractor_service._get_validated_year(None) is None

        # Test with invalid year (should raise ValidationError)
        with pytest.raises(ValidationError):
            extractor_service._get_validated_year(1899)

    def test_is_data_expired(self, extractor_service):
        """
        Tests the _is_data_expired method with different datetime scenarios
        """
        old_datetime = pd.Timestamp.now() - pd.Timedelta(minutes=31)
        extractor_service._duck_db.fetch_data.return_value = pd.DataFrame({'datetime': [old_datetime]})
        assert extractor_service._is_data_expired() is True

        recent_datetime = pd.Timestamp.now() - pd.Timedelta(minutes=29)
        extractor_service._duck_db.fetch_data.return_value = pd.DataFrame({'datetime': [recent_datetime]})
        assert extractor_service._is_data_expired() is False

    def test_extract_data_with_invalid_year(self, app, extractor_service):
        """
        Tests extract_data method with an invalid year input
        """
        with app.app_context():
            response = extractor_service.extract_data('processing', 'hybrid_americans', year=1899)
            assert response.status_code == 400
            assert 'year' in response.get_data(as_text=True)
