import asyncio
import logging
import uuid
from logging.config import dictConfig

import pytest

from core.logger import LOGGING
from tests.functional.settings import test_settings
from tests.functional.testdata.query_data import QueryData

dictConfig(LOGGING)
log = logging.getLogger(__name__)
query = QueryData()


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'count': 50, 'size': 100},
                {'status': 200, 'length': 50}
        ),
        (
                {'count': 50, 'size': 10, 'name': 'Ann'},
                {'status': 200, 'length': 10}
        ),
        (
                {'count': 50, 'size': 99999},
                {'status': 422, 'length': 1}
        ),
        (
                {'count': 50, 'size': 0},
                {'status': 422, 'length': 1}
        ),
        (
                {'count': 50, 'size': -1},
                {'status': 422, 'length': 1}
        )

    ]
)
@pytest.mark.asyncio
async def test_genre_all(fill_test_data, make_get_request, clear_elastic, query_data, expected_answer):
    await clear_elastic
    log.info('Elastic clear')
    # Генерируем данные для ES
    await fill_test_data(es_index='genres', count=query_data['count'], query_data=query.GENRE)
    await asyncio.sleep(1)  # Pause to fill the database
    log.info('Elastic is filled')

    url = f'http://{test_settings.service_url}:8000/api/v1/genres/'
    query_param = {'page[number]': '1',
                   'page[size]': query_data['size']
                   }

    response = await make_get_request(url, query_param)
    resp = await response.json()

    # Проверяем ответ
    assert response.status == expected_answer['status']
    assert len(resp) == expected_answer['length']


@pytest.mark.asyncio
async def test_genre_id(fill_test_data, make_get_request):
    # Генерируем данные для ES
    id_genre = str(uuid.uuid4())
    await fill_test_data(es_index='genres', count=1, query_data=query.GENRE, es_id_field=id_genre)
    await asyncio.sleep(1)  # Pause to fill the database

    url = f'http://{test_settings.service_url}:8000/api/v1/genres/{id_genre}'
    response = await make_get_request(url)
    resp = await response.json()
    # Проверяем ответ
    assert response.status == 200
    assert resp['id'] == id_genre


@pytest.mark.asyncio
async def test_genre_redis(fill_test_data, make_get_request, clear_elastic):
    # Генерируем данные для ES
    id_genre = str(uuid.uuid4())
    await fill_test_data(es_index='genres', count=1, query_data=query.GENRE, es_id_field=id_genre)
    await asyncio.sleep(1)  # Pause to fill the database

    url = f'http://{test_settings.service_url}:8000/api/v1/genres/{id_genre}'
    response = await make_get_request(url)
    resp = await response.json()
    # Проверяем ответ
    assert response.status == 200
    assert resp['id'] == id_genre
    # Очистка Elastic для проверки Redis
    await clear_elastic
    log.info('Elastic clear')
    url = f'http://{test_settings.service_url}:8000/api/v1/genres/{id_genre}'
    response = await make_get_request(url)
    resp = await response.json()
    assert response.status == 200
    assert resp['id'] == id_genre
