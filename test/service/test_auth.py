from service.auth import AuthService
import pytest
from unittest.mock import patch


class TestAuthService(object):
    @pytest.fixture
    def auth_service(self):
        return AuthService()

    @patch('service.auth.create_access_token')
    def test_authenticate_success(self, mock_create_token, auth_service):
        """
        Checks if a valid user receives an access token and code 200
        """
        mock_create_token.return_value = 'mocked_token'
        credentials = {'username': 'admin', 'password': 'admin'}

        result, status_code = auth_service.authenticate(credentials)

        assert status_code == 200
        assert result == {'access_token': 'mocked_token'}
        mock_create_token.assert_called_once()

    def test_authenticate_invalid_credentials(self, auth_service):
        """
        Checks if invalid credentials return error and code 401
        """
        invalid_credentials = {'username': 'wrong', 'password': 'wrong'}

        result, status_code = auth_service.authenticate(invalid_credentials)

        assert status_code == 401
        assert result == {'error': 'Invalid credentials'}

    def test_authenticate_missing_credentials(self, auth_service):
        """
        Checks if incomplete credentials return error and code 401
        """
        incomplete_credentials = {'username': 'admin'}

        result, status_code = auth_service.authenticate(incomplete_credentials)

        assert status_code == 401
        assert result == {'error': 'Invalid credentials'}
