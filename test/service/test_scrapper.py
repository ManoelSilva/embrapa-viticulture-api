from service.scrapper import EMBRAPAScrapperService
import pytest
from unittest.mock import patch, Mock
import pandas as pd


class TestEMBRAPAScrapperService(object):
    @pytest.fixture
    def scrapper_service(self):
        return EMBRAPAScrapperService()

    @patch('service.scrapper.requests.get')
    @patch('service.scrapper.BeautifulSoup')
    @patch('service.scrapper.pd.read_html')
    def test_scrape_and_parse_tables_success(self, mock_read_html, mock_bs, mock_get, scrapper_service):
        """
        Checks if data is correctly scraped and parsed when valid parameters are provided
        """
        data = [{'col1': 1, 'col2': 'a'}, {'col1': 2, 'col2': 'b'}]
        mock_df = pd.DataFrame(data)
        mock_response = Mock()
        mock_soup = Mock()
        mock_table = Mock()

        mock_get.return_value = mock_response
        mock_bs.return_value = mock_soup
        mock_soup.find.return_value = mock_table
        mock_read_html.return_value = [mock_df]

        result = scrapper_service.scrape_and_parse_tables('2023', 'import', 'grape_juice')

        assert result.equals(mock_df)
        mock_get.assert_called_once()
        mock_soup.find.assert_called_once_with('table', class_='tb_base tb_dados')
        mock_read_html.assert_called_once()

    @patch('service.scrapper.requests.get')
    def test_scrape_and_parse_tables_invalid_resource(self, mock_get, scrapper_service):
        """
        Checks if empty DataFrame is returned when invalid resource is provided
        """
        result = scrapper_service.scrape_and_parse_tables('2023', 'invalid_resource')

        assert result.empty
        mock_get.assert_not_called()

    @patch('service.scrapper.requests.get')
    def test_scrape_and_parse_tables_request_exception(self, mock_get, scrapper_service):
        """
        Checks if empty DataFrame is returned when request fails
        """
        mock_get.side_effect = Exception('Connection error')

        result = scrapper_service.scrape_and_parse_tables('2023', 'import', 'grape_juice')

        assert result.empty
        mock_get.assert_called_once()

    @patch('service.scrapper.requests.get')
    @patch('service.scrapper.BeautifulSoup')
    def test_scrape_and_parse_tables_no_table_found(self, mock_bs, mock_get, scrapper_service):
        """
        Checks if empty DataFrame is returned when no table is found
        """
        mock_response = Mock()
        mock_soup = Mock()
        mock_soup.find.return_value = None

        mock_get.return_value = mock_response
        mock_bs.return_value = mock_soup

        result = scrapper_service.scrape_and_parse_tables('2023', 'import', 'grape_juice')

        assert result.empty
        mock_get.assert_called_once()
        mock_soup.find.assert_called_once_with('table', class_='tb_base tb_dados')
