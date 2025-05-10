from unittest.mock import MagicMock
from flask import Flask
import pytest
from flask_jwt_extended import create_access_token, JWTManager

from src.routes.api_processing import ApiProcessingRoutes
from src.service.extractor import EMBRAPAExtractorService


class TestApiProcessingRoutes(object):
    @pytest.fixture
    def app(self):
        """Fixture to create a Flask app instance for testing"""
        app = Flask(__name__)
        app.config['JWT_SECRET_KEY'] = 'test-secret'

        JWTManager(app)

        extractor_service = MagicMock(spec=EMBRAPAExtractorService)
        api_routes = ApiProcessingRoutes(extractor_service)
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

    def test_get_vines(self, app):
        """
        Test the get_vines method
        """
        app_instance, extractor_service = app
        mock_data = {'data': 'mocked vines data'}
        extractor_service.extract_data.return_value = mock_data

        with app_instance.app_context():
            client = app_instance.test_client()
            access_token = create_access_token(identity='test_user')
            client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

            response = client.get('/api/processing/vines')
            assert response.status_code == 200
            assert response.get_json() == mock_data
            extractor_service.extract_data.assert_called_once_with(resource='processing', sub_resource='vines',
                                                                   year=None)

    def test_get_hybrid_americans(self, app):
        """
        Test the get_hybrid_americans method
        """
        app_instance, extractor_service = app
        mock_data = {'data': 'mocked hybrid americans data'}
        extractor_service.extract_data.return_value = mock_data

        with app_instance.app_context():
            client = app_instance.test_client()
            access_token = create_access_token(identity='test_user')
            client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

            response = client.get('/api/processing/hybrid_americans')
            assert response.status_code == 200
            assert response.get_json() == mock_data
            extractor_service.extract_data.assert_called_once_with(resource='processing',
                                                                   sub_resource='hybrid_americans',
                                                                   year=None)

    def test_get_table_grapes(self, app):
        """
        Test the get_table_grapes method
        """
        app_instance, extractor_service = app
        mock_data = {'data': 'mocked table grapes data'}
        extractor_service.extract_data.return_value = mock_data

        with app_instance.app_context():
            client = app_instance.test_client()
            access_token = create_access_token(identity='test_user')
            client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

            response = client.get('/api/processing/table_grapes')
            assert response.status_code == 200
            assert response.get_json() == mock_data
            extractor_service.extract_data.assert_called_once_with(resource='processing', sub_resource='table_grapes',
                                                                   year=None)

    def test_get_unclassified(self, app):
        """
        Test the get_unclassified method
        """
        app_instance, extractor_service = app
        mock_data = {'data': 'mocked unclassified data'}
        extractor_service.extract_data.return_value = mock_data

        with app_instance.app_context():
            client = app_instance.test_client()
            access_token = create_access_token(identity='test_user')
            client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

            response = client.get('/api/processing/unclassified')
            assert response.status_code == 200
            assert response.get_json() == mock_data
            extractor_service.extract_data.assert_called_once_with(resource='processing', sub_resource='unclassified',
                                                                   year=None)

    def test_get_url_prefix(self):
        """
        Test if the get_url_prefix method returns the correct URL prefix
        """
        extractor_service = MagicMock(spec=EMBRAPAExtractorService)
        api_routes = ApiProcessingRoutes(extractor_service)

        assert api_routes.get_url_prefix() == '/api/processing'

    def test_get_blueprint_name(self):
        """
        Test if the get_blueprint_name method returns the correct blueprint name
        """
        extractor_service = MagicMock(spec=EMBRAPAExtractorService)
        api_routes = ApiProcessingRoutes(extractor_service)

        assert api_routes.get_blueprint_name() == 'api_processing'
