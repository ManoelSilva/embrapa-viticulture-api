from io import StringIO

import requests
from bs4 import BeautifulSoup
import pandas as pd
from loguru import logger


class EMBRAPAScrapperService(object):
    _URL = 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao={}{}{}'
    _YEAR_PARAM = '&ano={}'
    _SUB_OPTIONS_PARAM = '&subopcao={}'

    _OPTIONS_MAP = {
        'production': {'option': 'opt_02'},
        'processing': {
            'option': 'opt_03',
            'sub_options': {
                'vines': 'subopt_01',
                'hybrid_americans': 'subopt_02',
                'table_grapes': 'subopt_03',
                'unclassified': 'subopt_04'
            }
        },
        'commercialization': {'option': 'opt_04'},
        'import': {
            'option': 'opt_05',
            'sub_options': {
                'table_wines': 'subopt_01',
                'sparkling': 'subopt_02',
                'fresh_grapes': 'subopt_03',
                'raisins': 'subopt_04',
                'grape_juice': 'subopt_05'
            }
        },
        'export': {
            'option': 'opt_06',
            'sub_options': {
                'table_wines': 'subopt_01',
                'sparkling': 'subopt_02',
                'fresh_grapes': 'subopt_03',
                'grape_juice': 'subopt_04'
            }
        }
    }

    def scrape_and_parse_tables(self, year: str, resource: str, sub_resource: str = None) -> pd.DataFrame:
        df = pd.DataFrame()
        try:
            logger.info(f'Scraping data for resource: {resource}, sub_resource: {sub_resource}, year: {year}')
            option_map = self._OPTIONS_MAP.get(resource)
            option = option_map.get('option')
            sub_resource = option_map.get('sub_options').get(sub_resource) if sub_resource else None

            year_param = self._YEAR_PARAM.format(year) if year else ''
            sub_options_param = self._SUB_OPTIONS_PARAM.format(sub_resource) if sub_resource else ''
            response = requests.get(self._URL.format(option, year_param, sub_options_param))

            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', class_='tb_base tb_dados')

            df = pd.read_html(StringIO(str(table)))[0]
        except Exception as e:
            logger.error('Exception threw while scrapping data: ', e)
        return df
