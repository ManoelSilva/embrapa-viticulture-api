from flask import request
from flask_jwt_extended import jwt_required

from routes.api_routes import BaseApiRoutes


class ApiImportRoutes(BaseApiRoutes):
    def get_url_prefix(self):
        return '/api/import'

    def get_blueprint_name(self):
        return 'api_import'

    def register_routes(self):
        @self.api_bp.route('/table_wines', methods=['GET'])
        @jwt_required()
        def get_table_grapes():
            return self._extractor.extract_data(resource='import', sub_resource='table_wines',
                                                year=self._get_year_param(request))

        @self.api_bp.route('/sparkling', methods=['GET'])
        @jwt_required()
        def get_sparkling():
            return self._extractor.extract_data(resource='import', sub_resource='sparkling',
                                                year=self._get_year_param(request))

        @self.api_bp.route('/fresh_grapes', methods=['GET'])
        @jwt_required()
        def get_fresh_grapes():
            return self._extractor.extract_data(resource='import', sub_resource='fresh_grapes',
                                                year=self._get_year_param(request))

        @self.api_bp.route('/raisins', methods=['GET'])
        @jwt_required()
        def get_raisins():
            return self._extractor.extract_data(resource='import', sub_resource='raisins',
                                                year=self._get_year_param(request))

        @self.api_bp.route('/grape_juice', methods=['GET'])
        @jwt_required()
        def get_grape_juice():
            return self._extractor.extract_data(resource='import', sub_resource='grape_juice',
                                                year=self._get_year_param(request))
