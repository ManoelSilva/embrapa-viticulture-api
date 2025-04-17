from duckdb.experimental.spark import DataFrame
from flask import jsonify, Response

from service.duck_db import DuckDBService
from service.scrapper import EMBRAPAScrapperService


class EMBRAPAExtractorService(object):

    def __init__(self, duck_db: DuckDBService):
        self._duck_db = duck_db
        self._scrapper = EMBRAPAScrapperService()

    def extract_data(self, resource: str, sub_resource: str = None, year: str = None) -> Response:
        duck_db_views = self._duck_db.get_views()
        view_name = '_'.join(filter(None, [resource, sub_resource, year]))
        if view_name in duck_db_views:
            data = self._duck_db.fetch_data(view_name)
            if data is None:
                data = self._scrape_and_load_data(resource, sub_resource, view_name, year)
        else:
            data = self._scrape_and_load_data(resource, sub_resource, view_name, year)
        return jsonify(data.to_dict(orient='records'))

    def _scrape_and_load_data(self, resource: str, sub_resource: str, table_name: str, year: str) -> DataFrame:

        data = self._scrapper.scrape_and_parse_tables(resource=resource, sub_resource=sub_resource,
                                                      year=year)
        self._duck_db.create_dataframe_view(table_name, data)
        return data
