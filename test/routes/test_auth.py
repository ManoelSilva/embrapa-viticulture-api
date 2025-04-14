import pytest
from flask import Flask
from routes.auth import auth_bp, auth_service
from service.auth import AuthService
from unittest.mock import Mock


class TestAuthRoutes(object):
    @pytest.fixture
    def app(self):
        app = Flask(__name__)
        app.config['PROPAGATE_EXCEPTIONS'] = True
        app.register_blueprint(auth_bp)
        return app

    @pytest.fixture
    def client(self, app):
        return app.test_client()

    @pytest.fixture(autouse=True)
    def setup_auth_service(self):
        self.mock_auth_service = Mock(spec=AuthService)
        self.original_service = auth_service
        import routes.auth
        routes.auth.auth_service = self.mock_auth_service
        yield
        routes.auth.auth_service = self.original_service

    def test_login_success(self, client):
        """
        Tests successful login scenario
        """
        credentials = {'username': 'admin', 'password': 'admin'}
        mock_response = ({'access_token': 'test_token'}, 200)
        self.mock_auth_service.authenticate.return_value = mock_response

        response = client.post('/login', json=credentials)

        assert response.status_code == 200
        assert response.get_json() == {'access_token': 'test_token'}
        self.mock_auth_service.authenticate.assert_called_once_with(credentials)

    def test_login_invalid_credentials(self, client):
        """
        Tests login failure scenario
        """
        credentials = {'username': 'wrong', 'password': 'wrong'}
        mock_response = ({'error': 'Invalid credentials'}, 401)
        self.mock_auth_service.authenticate.return_value = mock_response

        response = client.post('/login', json=credentials)

        assert response.status_code == 401
        assert response.get_json() == {'error': 'Invalid credentials'}
        self.mock_auth_service.authenticate.assert_called_once_with(credentials)

    def test_login_missing_credentials(self, client):
        """
        Tests missing credentials scenario
        """
        mock_response = ({'error': 'Invalid credentials'}, 401)
        self.mock_auth_service.authenticate.return_value = mock_response

        response = client.post('/login', json={})

        assert response.status_code == 401
        assert response.get_json() == {'error': 'Invalid credentials'}
        self.mock_auth_service.authenticate.assert_called_once_with({})
