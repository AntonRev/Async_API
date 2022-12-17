import logging.config
import time

from core.logger import LOGGING
from elasticsearch import Elasticsearch
from tests.functional.settings import TestSettings

es_host = TestSettings().es_host
logging.config.dictConfig(LOGGING)
log = logging.getLogger('')

if __name__ == '__main__':
    es_client = Elasticsearch(hosts=es_host, validate_cert=False, use_ssl=False)
    while True:
        if es_client.ping():
            break
        time.sleep(1)
        log.info("Waiting start Elasticsearch")
    log.info("Elasticsearch connected")
