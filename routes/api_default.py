from flask import request
from flask_jwt_extended import jwt_required

from routes.api_routes import BaseApiRoutes


class ApiDefaultRoutes(BaseApiRoutes):
    def get_url_prefix(self):
        return '/api'

    def get_blueprint_name(self):
        return 'api_default'

    def register_routes(self):
        @self.api_bp.route('/production', methods=['GET'])
        @jwt_required()
        def get_production():
            return self._extractor.extract_data(resource='production', year=self._get_year_param(request))

        @self.api_bp.route('/commercialization', methods=['GET'])
        @jwt_required()
        def get_commercialization():
            return self._extractor.extract_data(resource='commercialization', year=self._get_year_param(request))
