from unittest.mock import MagicMock
from flask import Flask
import pytest
from flask_jwt_extended import create_access_token, JWTManager
from routes.auth import ApiAuthRoutes
from service.auth import AuthService


class TestAuthRoutes(object):
    @pytest.fixture
    def app(self):
        """Fixture to create a Flask app instance for testing"""
        app = Flask(__name__)
        app.config['JWT_SECRET_KEY'] = 'test-secret'

        JWTManager(app)

        auth_service = MagicMock(spec=AuthService)
        api_routes = ApiAuthRoutes(auth_service)
        app.register_blueprint(api_routes.api_bp, url_prefix=api_routes.get_url_prefix())
        return app, auth_service

    @pytest.fixture
    def client(self, app):
        """Fixture to create a test client with JWT authentication"""
        app_instance, _ = app
        client = app_instance.test_client()
        access_token = create_access_token(identity='test_user')
        client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
        return client

    def test_register(self, app):
        """
        Test the register method
        """
        app_instance, auth_service = app
        mock_response = {'message': 'User registered successfully'}
        auth_service.register_user.return_value = (mock_response, 201)

        with app_instance.app_context():
            client = app_instance.test_client()
            response = client.post('/api/auth/register', json={'username': 'test_user', 'password': 'test_pass'})

            assert response.status_code == 201
            assert response.get_json() == mock_response
            auth_service.register_user.assert_called_once_with('test_user', 'test_pass')

    def test_login_success(self, app):
        """
        Test the login method with valid credentials
        """
        app_instance, auth_service = app
        mock_response = {'access_token': 'test_token'}
        auth_service.authenticate_user.return_value = (mock_response, 200)

        with app_instance.app_context():
            client = app_instance.test_client()
            response = client.post('/api/auth/login', json={'username': 'test_user', 'password': 'test_pass'})

            assert response.status_code == 200
            assert response.get_json() == mock_response
            auth_service.authenticate_user.assert_called_once_with('test_user', 'test_pass')

    def test_login_invalid_credentials(self, app):
        """
        Test the login method with invalid credentials
        """
        app_instance, auth_service = app
        mock_response = {'error': 'Invalid credentials'}
        auth_service.authenticate_user.return_value = (mock_response, 401)

        with app_instance.app_context():
            client = app_instance.test_client()
            response = client.post('/api/auth/login', json={'username': 'wrong_user', 'password': 'wrong_pass'})

            assert response.status_code == 401
            assert response.get_json() == mock_response
            auth_service.authenticate_user.assert_called_once_with('wrong_user', 'wrong_pass')

    def test_get_url_prefix(self):
        """
        Test if the get_url_prefix method returns the correct URL prefix
        """
        auth_service = MagicMock(spec=AuthService)
        api_routes = ApiAuthRoutes(auth_service)

        assert api_routes.get_url_prefix() == '/api/auth'

    def test_get_blueprint_name(self):
        """
        Test if the get_blueprint_name method returns the correct blueprint name
        """
        auth_service = MagicMock(spec=AuthService)
        api_routes = ApiAuthRoutes(auth_service)

        assert api_routes.get_blueprint_name() == 'api_auth'
