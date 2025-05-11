from unittest.mock import patch, MagicMock
import os

# Mock the entire duck_db module before any imports
mock_duckdb = MagicMock()
with patch('src.service.duck_db.DuckDBService', mock_duckdb):
    import pytest
    from flask_jwt_extended import create_access_token, JWTManager
    from src.app import App


class TestApp(object):
    @pytest.fixture
    def mock_logger(self):
        """Fixture to mock the logger"""
        with patch('src.app.logger') as mock:
            yield mock

    @pytest.fixture
    def app(self, mock_logger):
        """Fixture to create a Flask app instance for testing"""
        app_instance = App()
        app = app_instance.create_app()
        app.config['TESTING'] = True
        app.config['JWT_SECRET_KEY'] = 'test-secret'
        JWTManager(app)
        return app

    @pytest.fixture
    def client(self, app):
        """Fixture to create a test client with JWT authentication"""
        with app.test_client() as client:
            with app.app_context():
                access_token = create_access_token(identity='test_user')
                client.environ_base = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
                yield client

    def test_app_creation(self, mock_logger):
        """
        Test if the Flask application is created successfully
        """
        app_instance = App()
        assert app_instance.app is not None
        assert isinstance(app_instance.app.config, dict)
        mock_logger.remove.assert_called_once_with(0)
        mock_logger.add.assert_called_once()

    def test_blueprints_registered(self, mock_logger):
        """
        Test if blueprints are registered
        """
        app_instance = App()
        blueprint_names = set(bp.name for bp in app_instance.app.blueprints.values())
        expected_blueprints = {
            'api_auth', 'api_default', 'api_exporting',
            'api_import', 'swagger_ui', 'api_processing'
        }
        assert blueprint_names.issuperset(expected_blueprints)
        mock_logger.remove.assert_called_once_with(0)
        mock_logger.add.assert_called_once()

    def test_app_logging_configuration(self, mock_logger):
        """
        Test if logging is properly configured during app initialization
        """
        app_instance = App()
        mock_logger.remove.assert_called_once_with(0)
        mock_logger.add.assert_called_once()
        assert hasattr(app_instance, 'app')

    def test_jwt_configuration(self, mock_logger):
        """
        Test if JWT is properly configured
        """
        app_instance = App()
        flask_app = app_instance.create_app()
        assert 'JWT_SECRET_KEY' in flask_app.config
        mock_logger.remove.assert_called_once_with(0)
        mock_logger.add.assert_called_once()

    def test_root_redirects_to_swagger(self, mock_logger):
        """
        Testa se a rota '/' faz redirect para '/swagger'
        """
        app_instance = App()
        app = app_instance.create_app()
        with app.test_client() as client:
            response = client.get('/')
            assert response.status_code == 302  # HTTP 302 Found (redirect)
            assert response.headers['Location'].endswith('/swagger')
