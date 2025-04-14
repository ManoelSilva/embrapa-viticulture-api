from flask import request
from flask_jwt_extended import jwt_required

from routes.api_routes import BaseApiRoutes


class ApiProcessingRoutes(BaseApiRoutes):
    def get_url_prefix(self):
        return '/api/processing'

    def get_blueprint_name(self):
        return 'api_processing'

    def register_routes(self):
        @self.api_bp.route('/vines', methods=['GET'])
        @jwt_required()
        def get_vines():
            return self._extractor.extract_data(resource='processing', sub_resource='vines',
                                                year=self._get_year_param(request))

        @self.api_bp.route('/hybrid_americans', methods=['GET'])
        @jwt_required()
        def get_hybrid_americans():
            return self._extractor.extract_data(resource='processing', sub_resource='hybrid_americans',
                                                year=self._get_year_param(request))

        @self.api_bp.route('/table_grapes', methods=['GET'])
        @jwt_required()
        def get_table_grapes():
            return self._extractor.extract_data(resource='processing', sub_resource='table_grapes',
                                                year=self._get_year_param(request))

        @self.api_bp.route('/unclassified', methods=['GET'])
        @jwt_required()
        def get_unclassified():
            return self._extractor.extract_data(resource='processing', sub_resource='unclassified',
                                                year=self._get_year_param(request))
