import os
from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    PROJECT_NAME: str = Field('movies', env='PROJECT_NAME')
    # Настройки Redis
    REDIS_HOST: str = Field('127.0.0.1', env='REDIS_HOST')
    REDIS_PORT: int = Field(6379, env='REDIS_PORT')
    CACHE_EXPIRE_IN_SECONDS: int = Field(300, env='CACHE_EXPIRE_IN_SECONDS')  # 5 минут
    # Настройки Elasticsearch
    ELASTIC_HOST: str = Field('127.0.0.1', env='ELASTIC_HOST')
    ELASTIC_PORT: int = Field(9200, env='ELASTIC_PORT')
    # Корень проекта
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    JWT_PUBLIC_KEY: str = Field('public_key', env='JWT_PUBLIC_KEY')

config = Settings()
