from duckdb.experimental.spark import DataFrame
from flask import jsonify, Response

import pandas as pd
from loguru import logger
from pydantic import ValidationError
from requests import RequestException

from src.model.year_request import YearRequest
from src.service.duck_db import DuckDBService
from src.service.scrapper import EMBRAPAScrapperService


class EMBRAPAExtractorService(object):
    HALF_HOUR = 1800
    BAD_REQUEST = 400

    def __init__(self, duck_db: DuckDBService):
        self._duck_db = duck_db
        self._scrapper = EMBRAPAScrapperService()

    def extract_data(self, resource: str, sub_resource: str = None, year: int = None) -> Response:
        try:
            validated_year = self._get_validated_year(year)
            duck_db_tables = self._duck_db.get_tables()
            table_name = '_'.join(filter(None, [resource, sub_resource, validated_year]))
            if table_name in duck_db_tables:
                data = self._duck_db.fetch_data(table_name)
                if data is None or self._is_data_expired():
                    data = self._scrape_and_load_data(resource, sub_resource, table_name, validated_year)
            else:
                data = self._scrape_and_load_data(resource, sub_resource, table_name, validated_year)
            return jsonify(data.to_dict(orient='records'))
        except ValidationError as e:
            return Response(e.json(), status=self.BAD_REQUEST)

    @staticmethod
    def _get_validated_year(year: int) -> str:
        validated_year = YearRequest(year=year).year
        return str(validated_year) if validated_year else None

    def _scrape_and_load_data(self, resource: str, sub_resource: str, table_name: str, year: str) -> DataFrame:
        try:
            data = self._scrapper.scrape_and_parse_tables(resource=resource, sub_resource=sub_resource,
                                                          year=year)
            self._duck_db.create_dataframe_table(table_name, data)
        except RequestException:
            logger.error(
                f'Error while scrapping data for resource: {resource}, sub_resource: {sub_resource}, year: {year}. '
                f'Fetching from database instead.')
            data = self._duck_db.fetch_data(table_name)
        return data

    def _is_data_expired(self):
        return (pd.Timestamp.now() - pd.to_datetime(
            self._duck_db.fetch_data('db_datetime').get('datetime')).max()).total_seconds() > self.HALF_HOUR
