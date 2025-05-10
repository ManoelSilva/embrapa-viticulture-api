from flask import Blueprint, Request
from abc import ABC, abstractmethod

from src.service.extractor import EMBRAPAExtractorService


class BaseApiRoutes(ABC):
    def __init__(self, extractor: EMBRAPAExtractorService | None):
        self.api_bp = Blueprint(self.get_blueprint_name(), __name__)
        self._extractor = extractor
        self.register_routes()

    @abstractmethod
    def register_routes(self):
        """Method that must be implemented by child classes to register routes"""
        pass

    @abstractmethod
    def get_blueprint_name(self) -> str:
        """Method that returns the name of the blueprint"""
        pass

    @abstractmethod
    def get_url_prefix(self) -> str:
        """Method that returns the URL prefix for the routes"""
        pass

    @staticmethod
    def _get_year_param(request: Request) -> str | None:
        """Helper method to get the year parameter from the request"""
        return request.args.get('year')
