from flask import request
from flask_jwt_extended import jwt_required

from src.routes.api_routes import BaseApiRoutes


class ApiExportingRoutes(BaseApiRoutes):
    def get_url_prefix(self):
        return '/api/exporting'

    def get_blueprint_name(self):
        return 'api_exporting'

    def register_routes(self):
        @self.api_bp.route('/table_wines', methods=['GET'])
        @jwt_required()
        def get_table_wines():
            return self._extractor.extract_data(resource='export', sub_resource='table_wines',
                                                year=self._get_year_param(request))

        @self.api_bp.route('/sparkling', methods=['GET'])
        @jwt_required()
        def get_sparkling():
            return self._extractor.extract_data(resource='export', sub_resource='sparkling',
                                                year=self._get_year_param(request))

        @self.api_bp.route('/fresh_grapes', methods=['GET'])
        @jwt_required()
        def get_fresh_grapes():
            return self._extractor.extract_data(resource='export', sub_resource='fresh_grapes',
                                                year=self._get_year_param(request))

        @self.api_bp.route('/grape_juice', methods=['GET'])
        @jwt_required()
        def get_grape_juice():
            return self._extractor.extract_data(resource='export', sub_resource='grape_juice',
                                                year=self._get_year_param(request))
