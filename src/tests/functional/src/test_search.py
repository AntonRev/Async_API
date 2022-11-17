import asyncio
import logging
from logging.config import dictConfig

import pytest
from core.logger import LOGGING
from tests.functional.settings import test_settings
from tests.functional.testdata.query_data import QueryData

dictConfig(LOGGING)
log = logging.getLogger(__name__)
query = QueryData()


@pytest.mark.asyncio
async def test_search(fill_test_data, make_get_request, clear_elastic):
    await clear_elastic
    log.info('Elastic clear')
    # Генерируем данные для ES
    await fill_test_data(es_index='movies', count=70, query_data=query.FILM)
    await asyncio.sleep(1)  # Pause to fill the database

    url = f'http://{test_settings.service_url}:8000/api/v1/films/search?'
    query_data = {'query': 'The Star',
                  'page[number]': '1',
                  'page[size]': '50'
                  }

    response = await make_get_request(url, query_data)
    resp = await response.json()

    # Проверяем ответ
    assert response.status == 200
    assert len(resp) == 50
