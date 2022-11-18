import asyncio
import json
import logging
import uuid

import aiohttp
import pytest_asyncio
from aiohttp import ClientSession
from elasticsearch import AsyncElasticsearch
from tests.functional.settings import test_settings
from tests.functional.testdata.mapping import Mapping

map = Mapping()
log = logging.getLogger(__name__)


@pytest_asyncio.fixture
def fill_test_data(es_client: AsyncElasticsearch):
    async def fill(es_index: str, count: int, query_data: str, es_id_field=None):
        """
        es_id_field for testing ID, use with count=1
        """
        # TODO: вместо query_data использовать библиотеку factory-boy
        es_data = [query_data for _ in range(count)]
        bulk_query = []
        for row in es_data:
            if es_id_field is None:
                _id = str(uuid.uuid4())
            else:
                _id = es_id_field
                row['id'] = es_id_field
            bulk_query.extend([
                json.dumps({'index': {'_index': es_index, '_id': _id}}),
                json.dumps(row)
            ])
        str_query = '\n'.join(bulk_query) + '\n'

        resp = await es_client.bulk(body=str_query)
        if resp['errors']:
            raise Exception('Ошибка записи данных в Elasticsearch: ', resp)
        return resp

    return fill


@pytest_asyncio.fixture
def make_get_request(http_client: ClientSession):
    async def get_request(uri: str, query_data: str):
        response = http_client.get(uri, params=query_data)
        return await response

    return get_request


@pytest_asyncio.fixture
async def clear_elastic(http_client):
    response = http_client.delete(f'http://{test_settings.es_host}:9200/_all')
    return response


@pytest_asyncio.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=f'{test_settings.es_host}',
                                validate_cert=False,
                                use_ssl=False)

    # Creating Indexes
    await client.indices.create(index='genres',
                                body=map.get_body(set=map.SETTINGS_SCHEMA, map=map.MAPPING_GENRE),
                                ignore=400)  # Ignore Error if index exist
    await client.indices.create(index='movies',
                                body=map.get_body(set=map.SETTINGS_SCHEMA, map=map.MAPPING_MUVIE),
                                ignore=400)
    await client.indices.create(index='persons',
                                body=map.get_body(set=map.SETTINGS_SCHEMA, map=map.MAPPING_PERSON),
                                ignore=400)

    yield client
    await client.close()


@pytest_asyncio.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def http_client():
    session = aiohttp.ClientSession()
    yield session
    await session.close()
