from unittest.mock import MagicMock
from flask import Flask
import pytest
from flask_jwt_extended import create_access_token, JWTManager

from src.routes.api_exporting import ApiExportingRoutes
from src.service.extractor import EMBRAPAExtractorService


class TestApiExportingRoutes(object):
    @pytest.fixture
    def app(self):
        """Fixture to create a Flask app instance for testing"""
        app = Flask(__name__)
        app.config['JWT_SECRET_KEY'] = 'test-secret'

        JWTManager(app)

        extractor_service = MagicMock(spec=EMBRAPAExtractorService)
        api_routes = ApiExportingRoutes(extractor_service)
        app.register_blueprint(api_routes.api_bp, url_prefix=api_routes.get_url_prefix())
        return app, extractor_service

    @pytest.fixture
    def client(self, app):
        """Fixture to create a test client with JWT authentication"""
        app_instance, _ = app
        client = app_instance.test_client()
        access_token = create_access_token(identity='test_user')
        client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
        return client

    def test_get_table_wines(self, app):
        """
        Test the get_table_wines method
        """
        app_instance, extractor_service = app
        mock_data = {'data': 'mocked table wines data'}
        extractor_service.extract_data.return_value = mock_data

        with app_instance.app_context():
            client = app_instance.test_client()
            access_token = create_access_token(identity='test_user')
            client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

            response = client.get('/api/exporting/table_wines')
            assert response.status_code == 200
            assert response.get_json() == mock_data
            extractor_service.extract_data.assert_called_once_with(resource='export', sub_resource='table_wines',
                                                                   year=None)

    def test_get_sparkling(self, app):
        """
        Test the get_sparkling method
        """
        app_instance, extractor_service = app
        mock_data = {'data': 'mocked sparkling data'}
        extractor_service.extract_data.return_value = mock_data

        with app_instance.app_context():
            client = app_instance.test_client()
            access_token = create_access_token(identity='test_user')
            client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

            response = client.get('/api/exporting/sparkling')
            assert response.status_code == 200
            assert response.get_json() == mock_data
            extractor_service.extract_data.assert_called_once_with(resource='export', sub_resource='sparkling',
                                                                   year=None)

    def test_get_fresh_grapes(self, app):
        """
        Test the get_fresh_grapes method
        """
        app_instance, extractor_service = app
        mock_data = {'data': 'mocked fresh grapes data'}
        extractor_service.extract_data.return_value = mock_data

        with app_instance.app_context():
            client = app_instance.test_client()
            access_token = create_access_token(identity='test_user')
            client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

            response = client.get('/api/exporting/fresh_grapes')
            assert response.status_code == 200
            assert response.get_json() == mock_data
            extractor_service.extract_data.assert_called_once_with(resource='export', sub_resource='fresh_grapes',
                                                                   year=None)

    def test_get_grape_juice(self, app):
        """
        Test the get_grape_juice method
        """
        app_instance, extractor_service = app
        mock_data = {'data': 'mocked grape juice data'}
        extractor_service.extract_data.return_value = mock_data

        with app_instance.app_context():
            client = app_instance.test_client()
            access_token = create_access_token(identity='test_user')
            client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

            response = client.get('/api/exporting/grape_juice')
            assert response.status_code == 200
            assert response.get_json() == mock_data
            extractor_service.extract_data.assert_called_once_with(resource='export', sub_resource='grape_juice',
                                                                   year=None)

    def test_get_url_prefix(self):
        """
        Test if the get_url_prefix method returns the correct URL prefix
        """
        extractor_service = MagicMock(spec=EMBRAPAExtractorService)
        api_routes = ApiExportingRoutes(extractor_service)

        assert api_routes.get_url_prefix() == '/api/exporting'

    def test_get_blueprint_name(self):
        """
        Test if the get_blueprint_name method returns the correct blueprint name
        """
        extractor_service = MagicMock(spec=EMBRAPAExtractorService)
        api_routes = ApiExportingRoutes(extractor_service)

        assert api_routes.get_blueprint_name() == 'api_exporting'
