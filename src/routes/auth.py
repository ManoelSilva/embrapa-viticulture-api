from flask import request, jsonify
from src.routes.api_routes import BaseApiRoutes
from src.service.auth import AuthService


class ApiAuthRoutes(BaseApiRoutes):
    def __init__(self, auth_service: AuthService):
        self._auth_service = auth_service
        super().__init__(None)

    def get_url_prefix(self):
        return '/api/auth'

    def get_blueprint_name(self):
        return 'api_auth'

    def register_routes(self):
        @self.api_bp.route('/register', methods=['POST'])
        def register():
            data = request.json
            response, status = self._auth_service.register_user(data.get('username'), data.get('password'))
            return jsonify(response), status

        @self.api_bp.route('/login', methods=['POST'])
        def login():
            data = request.json
            response, status = self._auth_service.authenticate_user(data.get('username'), data.get('password'))
            return jsonify(response), status
