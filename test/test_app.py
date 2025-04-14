import pytest
from flask_jwt_extended import create_access_token, JWTManager
from app import App
from unittest.mock import patch


class TestApp(object):
    @pytest.fixture
    def mock_logger(self):
        """Fixture to mock the logger"""
        with patch('app.logger') as mock:
            yield mock

    @pytest.fixture
    def app(self, mock_logger, app):
        """Fixture to create a Flask app instance for testing"""
        app_instance = App()
        app = app_instance.create_app()
        app.config['TESTING'] = True
        app.config['JWT_SECRET_KEY'] = 'test-secret'
        JWTManager(app)
        return app

    @pytest.fixture
    def client(self, app, client):
        """Fixture to create a test client with JWT authentication"""
        with app.test_client() as client:
            with app.app_context():
                access_token = create_access_token(identity='test_user')
                client.environ_base = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
                yield client

    @patch('app.logger')
    def test_app_creation(self, mock_logger):
        """
        Test if the Flask application is created successfully
        """
        app_instance = App()
        assert app_instance.app is not None
        assert isinstance(app_instance.app.config, dict)
        mock_logger.remove.assert_called_once_with(0)
        mock_logger.add.assert_called_once()

    @patch('app.logger')
    def test_blueprints_registered(self, mock_logger):
        """
        Test if blueprints are registered
        """
        app_instance = App()
        blueprint_names = set(bp.name for bp in app_instance.app.blueprints.values())
        expected_blueprints = {
            'auth', 'api_default', 'api_exporting',
            'api_import', 'swagger_ui', 'api_processing'
        }
        assert blueprint_names.issuperset(expected_blueprints)
        mock_logger.remove.assert_called_once_with(0)
        mock_logger.add.assert_called_once()

    @patch('app.logger')
    def test_app_logging_configuration(self, mock_logger):
        """
        Test if logging is properly configured during app initialization
        """
        app_instance = App()
        mock_logger.remove.assert_called_once_with(0)
        mock_logger.add.assert_called_once()
        assert hasattr(app_instance, 'app')

    @patch('app.logger')
    def test_jwt_configuration(self, mock_logger):
        """
        Test if JWT is properly configured
        """
        app_instance = App()
        flask_app = app_instance.create_app()
        assert 'JWT_SECRET_KEY' in flask_app.config
        mock_logger.remove.assert_called_once_with(0)
        mock_logger.add.assert_called_once()
