import os

from flask import Flask, send_from_directory, redirect
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from loguru import logger

from src.logger_serialize import serialize
from src.config.auth import AuthConfig
from src.routes.api_default import ApiDefaultRoutes
from src.routes.api_exporting import ApiExportingRoutes
from src.routes.api_import import ApiImportRoutes
from src.routes.api_processing import ApiProcessingRoutes
from src.routes.auth import ApiAuthRoutes
from src.service.auth import AuthService
from src.service.duck_db import DuckDBService
from src.service.extractor import EMBRAPAExtractorService


class App:
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.yml'

    def __init__(self):
        self.app = Flask(__name__)
        self._duckdb = DuckDBService()
        self._extractor = EMBRAPAExtractorService(self._duckdb)
        self._configure_logging()
        self._configure_app()
        self._register_blueprints()

    @staticmethod
    def _configure_logging():
        logger.remove(0)
        logger.add(serialize)

    def _configure_app(self):
        self.app.config.from_object(AuthConfig)
        JWTManager(self.app)

    def _register_blueprints(self):
        swagger_ui_blueprint = get_swaggerui_blueprint(self.SWAGGER_URL, self.API_URL)
        self.app.register_blueprint(swagger_ui_blueprint, url_prefix=self.SWAGGER_URL)

        auth_routes = ApiAuthRoutes(AuthService(self._duckdb))
        self.app.register_blueprint(auth_routes.api_bp, url_prefix=auth_routes.get_url_prefix())

        default_routes = ApiDefaultRoutes(self._extractor)
        self.app.register_blueprint(default_routes.api_bp, url_prefix=default_routes.get_url_prefix())

        exporting_routes = ApiExportingRoutes(self._extractor)
        self.app.register_blueprint(exporting_routes.api_bp, url_prefix=exporting_routes.get_url_prefix())

        import_routes = ApiImportRoutes(self._extractor)
        self.app.register_blueprint(import_routes.api_bp, url_prefix=import_routes.get_url_prefix())

        processing_routes = ApiProcessingRoutes(self._extractor)
        self.app.register_blueprint(processing_routes.api_bp, url_prefix=processing_routes.get_url_prefix())

    def create_app(self):
        @self.app.route('/static/swagger.yml')
        def send_swagger():
            return send_from_directory(os.path.dirname(__file__), './config/swagger.yml')

        @self.app.route('/')
        def root_swagger():
            return redirect('/swagger')

        return self.app


app = App().create_app()
