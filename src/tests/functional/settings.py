from logging.config import dictConfig

from pydantic import BaseSettings, Field
from tests.functional.logger import LOGGING


class TestSettings(BaseSettings):
    es_host: str = Field('127.0.0.1', env='ELASTIC_HOST')
    es_index: str = 'movies'

    redis_host: str = Field('127.0.0.1', env='REDIS_HOST')
    service_url: str = Field('127.0.0.1', env='FASTAPI_HOST')

    LOG_LEVEL: str = Field('DEBUG', env='LOG_LEVEL')


test_settings = TestSettings()
dictConfig(LOGGING)
