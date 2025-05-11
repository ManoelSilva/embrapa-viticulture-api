from unittest.mock import patch, Mock

import pandas as pd
import pytest
from bs4 import BeautifulSoup

from src.service.scrapper import EMBRAPAScrapperService


class TestEMBRAPAScrapperService(object):
    @pytest.fixture
    def scrapper_service(self):
        return EMBRAPAScrapperService()

    @patch('src.service.scrapper.requests.get')
    @patch('src.service.scrapper.pd.read_html')
    def test_scrape_and_parse_tables_success(self, mock_read_html, mock_get, scrapper_service):
        """
        Checks if data is correctly scraped and parsed when valid parameters are provided
        """
        # Mock HTML with table
        html_content = '''
        <html>
            <body>
                <table class="tb_base tb_dados">
                    <tr><td>col1</td><td>col2</td></tr>
                    <tr><td>1</td><td>a</td></tr>
                    <tr><td>2</td><td>b</td></tr>
                </table>
            </body>
        </html>
        '''
        mock_response = Mock()
        mock_response.content = html_content.encode()
        mock_get.return_value = mock_response

        data = [{'col1': 1, 'col2': 'a'}, {'col1': 2, 'col2': 'b'}]
        mock_df = pd.DataFrame(data)
        mock_read_html.return_value = [mock_df]

        result = scrapper_service.scrape_and_parse_tables('2023', 'import', 'grape_juice')

        assert not result.empty
        assert len(result) == 2
        assert list(result.columns) == ['col1', 'col2']
        mock_get.assert_called_once()
        mock_read_html.assert_called_once()

    @patch('src.service.scrapper.requests.get')
    def test_scrape_and_parse_tables_invalid_resource(self, mock_get, scrapper_service):
        """
        Checks if AttributeError is raised when invalid resource is provided
        """
        with pytest.raises(AttributeError):
            scrapper_service.scrape_and_parse_tables('2023', 'invalid_resource')
        mock_get.assert_not_called()

    @patch('src.service.scrapper.requests.get')
    def test_scrape_and_parse_tables_request_exception(self, mock_get, scrapper_service):
        """
        Checks if request exception is propagated
        """
        mock_get.side_effect = Exception('Connection error')

        with pytest.raises(Exception) as exc_info:
            scrapper_service.scrape_and_parse_tables('2023', 'import', 'grape_juice')

        assert str(exc_info.value) == 'Connection error'
        mock_get.assert_called_once()

    @patch('src.service.scrapper.requests.get')
    @patch('src.service.scrapper.pd.read_html')
    def test_scrape_and_parse_tables_no_table_found(self, mock_read_html, mock_get, scrapper_service):
        """
        Checks if IndexError is raised when no table is found
        """
        # Mock HTML without table
        html_content = '<html><body>No table here</body></html>'
        mock_response = Mock()
        mock_response.content = html_content.encode()
        mock_get.return_value = mock_response
        mock_read_html.return_value = []

        with pytest.raises(IndexError):
            scrapper_service.scrape_and_parse_tables('2023', 'import', 'grape_juice')

        mock_get.assert_called_once()
        mock_read_html.assert_called_once()
