from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
import datetime
from src.service.duck_db import DuckDBService


class AuthService:
    def __init__(self, duckdb_service: DuckDBService):
        self._duckdb = duckdb_service

    def register_user(self, username: str, password: str) -> tuple[dict[str, str], int]:
        if not username or not password:
            return {'error': 'Username and password are required'}, 400

        if self._duckdb.user_exists(username):
            return {'error': 'User already exists'}, 400

        hashed_password = generate_password_hash(password)
        self._duckdb.insert_user(username, hashed_password)
        return {'message': 'User registered successfully'}, 201

    def authenticate_user(self, username: str, password: str) -> tuple[dict[str, str], int]:
        if not username or not password:
            return {'error': 'Username and password are required'}, 400

        users = self._duckdb.fetch_data('users')
        if users is None or username not in users['username'].values:
            return {'error': 'Invalid username or password'}, 401

        user = users[users['username'] == username].iloc[0]
        if not check_password_hash(user['password'], password):
            return {'error': 'Invalid username or password'}, 401

        expires = datetime.timedelta(hours=1)
        access_token = create_access_token(identity=username, expires_delta=expires)
        return {'access_token': access_token}, 200
