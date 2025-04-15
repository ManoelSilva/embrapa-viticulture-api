import datetime

from service.auth import AuthService
import pytest
from unittest.mock import patch, Mock
import pandas as pd


class TestAuthService(object):
    @pytest.fixture
    def auth_service(self):
        """Fixture to create an instance of AuthService with mocked dependencies"""
        duckdb_mock = Mock()
        return AuthService(duckdb_mock)

    def test_register_user_success(self, auth_service):
        """
        Checks if a user is successfully registered when valid data is provided
        """
        auth_service._duckdb.user_exists.return_value = False

        result, status_code = auth_service.register_user('new_user', 'password123')

        assert status_code == 201
        assert result == {'message': 'User registered successfully'}
        auth_service._duckdb.user_exists.assert_called_once_with('new_user')
        auth_service._duckdb.insert_user.assert_called_once()

    def test_register_user_existing_user(self, auth_service):
        """
        Checks if an error is returned when the user already exists
        """
        auth_service._duckdb.user_exists.return_value = True

        result, status_code = auth_service.register_user('existing_user', 'password123')

        assert status_code == 400
        assert result == {'error': 'User already exists'}
        auth_service._duckdb.user_exists.assert_called_once_with('existing_user')
        auth_service._duckdb.insert_user.assert_not_called()

    def test_register_user_missing_data(self, auth_service):
        """
        Checks if an error is returned when username or password is missing
        """
        result, status_code = auth_service.register_user('', '')

        assert status_code == 400
        assert result == {'error': 'Username and password are required'}
        auth_service._duckdb.user_exists.assert_not_called()
        auth_service._duckdb.insert_user.assert_not_called()

    @patch('service.auth.create_access_token')
    @patch('service.auth.check_password_hash', return_value=True)
    def test_authenticate_user_success(self, mock_check_password, mock_create_token, auth_service):
        """
        Checks if a valid user receives an access token
        """
        data = {'username': ['valid_user'], 'password': ['hashed_password']}
        users_df = pd.DataFrame(data)
        auth_service._duckdb.fetch_data.return_value = users_df

        mock_create_token.return_value = 'mocked_token'

        result, status_code = auth_service.authenticate_user('valid_user', 'password123')

        assert status_code == 200
        assert result == {'access_token': 'mocked_token'}
        auth_service._duckdb.fetch_data.assert_called_once_with('users')
        mock_check_password.assert_called_once_with('hashed_password', 'password123')
        mock_create_token.assert_called_once_with(identity='valid_user', expires_delta=datetime.timedelta(hours=1))

    def test_authenticate_user_invalid_credentials(self, auth_service):
        """
        Checks if an error is returned when invalid credentials are provided
        """
        data = {'username': ['valid_user'], 'password': ['hashed_password']}
        users_df = pd.DataFrame(data)
        auth_service._duckdb.fetch_data.return_value = users_df

        with patch('werkzeug.security.check_password_hash', return_value=False):
            result, status_code = auth_service.authenticate_user('valid_user', 'wrong_password')

            assert status_code == 401
            assert result == {'error': 'Invalid username or password'}
            auth_service._duckdb.fetch_data.assert_called_once_with('users')

    def test_authenticate_user_missing_data(self, auth_service):
        """
        Checks if an error is returned when username or password is missing
        """
        result, status_code = auth_service.authenticate_user('', '')

        assert status_code == 400
        assert result == {'error': 'Username and password are required'}
        auth_service._duckdb.fetch_data.assert_not_called()
