from aiohttp import ClientSession

from tests.functional.settings import test_settings


async def make_get_request(http_client: ClientSession, uri: str, query_data: str = None):
    response = http_client.get(uri, params=query_data)
    return await response


async def clear_elastic(http_client: ClientSession, index: str = "_all"):
    await http_client.delete(f'http://{test_settings.es_host}:9200/{index}')
