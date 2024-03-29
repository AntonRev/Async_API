import asyncio
import http
import logging
import uuid
from logging.config import dictConfig

import pytest

from configs.logger import LOGGING
from tests.functional.settings import test_settings
from tests.functional.src.common import clear_elastic, make_get_request
from tests.functional.testdata.query_data import QueryData

dictConfig(LOGGING)
log = logging.getLogger(__name__)
query = QueryData()
ES_INDEX = 'movies'


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'count': 50, 'size': 100, 'name': 'The Star'},
                {'status': http.HTTPStatus.OK, 'length': 50}
        ),
        (
                {'count': 50, 'size': 10, 'name': 'The Star'},
                {'status': http.HTTPStatus.OK, 'length': 10}
        ),
        (
                {'count': 50, 'size': 99999, 'name': 'The Star'},
                {'status': http.HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1}
        ),
        (
                {'count': 50, 'size': 0, 'name': 'The Star'},
                {'status': http.HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1}
        ),
        (
                {'count': 50, 'size': -1, 'name': 'The Star'},
                {'status': http.HTTPStatus.UNPROCESSABLE_ENTITY, 'length': 1}
        )

    ]
)
@pytest.mark.asyncio
async def test_search(fill_test_data, http_client, query_data, expected_answer):
    await clear_elastic(http_client, ES_INDEX)
    log.info('Elastic clear')
    # Генерируем данные для ES
    await fill_test_data(es_index=ES_INDEX, count=query_data['count'], query_data=query.FILM)
    await asyncio.sleep(1)  # Pause to fill the database

    url = f'http://{test_settings.service_url}:8000/api/v1/films/search?'
    query_datas = {'query': query_data['name'],
                   'page[number]': '1',
                   'page[size]': query_data['size']
                   }

    response = await make_get_request(http_client, url, query_datas)
    resp = await response.json()

    # Проверяем ответ
    assert response.status == expected_answer['status']
    assert len(resp) == expected_answer['length']


@pytest.mark.asyncio
async def test_film_id(fill_test_data, http_client):
    # Генерируем данные для ES
    id_film = str(uuid.uuid4())
    await fill_test_data(es_index=ES_INDEX, count=1, query_data=query.FILM, es_id_field=id_film)
    await asyncio.sleep(1)  # Pause to fill the database

    url = f'http://{test_settings.service_url}:8000/api/v1/films/{id_film}'
    response = await make_get_request(http_client, url)
    resp = await response.json()
    # Проверяем ответ
    assert response.status == http.HTTPStatus.OK
    assert resp['id'] == id_film


@pytest.mark.asyncio
async def test_film_redis(fill_test_data, http_client):
    # Генерируем данные для ES
    id_film = str(uuid.uuid4())
    await fill_test_data(es_index=ES_INDEX, count=1, query_data=query.FILM, es_id_field=id_film)
    await asyncio.sleep(1)  # Pause to fill the database

    url = f'http://{test_settings.service_url}:8000/api/v1/films/{id_film}'
    response = await make_get_request(http_client, url)
    resp = await response.json()

    # Проверяем ответ
    assert response.status == http.HTTPStatus.OK
    assert resp['id'] == id_film

    # Очистка Elastic для проверки Redis
    await clear_elastic(http_client, ES_INDEX)
    log.info('Elastic clear')
    url = f'http://{test_settings.service_url}:8000/api/v1/films/{id_film}'
    response = await make_get_request(http_client, url)
    resp = await response.json()
    assert response.status == http.HTTPStatus.OK
    assert resp['id'] == id_film
