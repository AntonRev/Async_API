import logging.config
import time

from core.logger import LOGGING
from redis import Redis
from redis.exceptions import ConnectionError
from tests.functional.settings import TestSettings

redis_host = TestSettings().redis_host
logging.config.dictConfig(LOGGING)
log = logging.getLogger('')

if __name__ == '__main__':
    r = Redis(redis_host)
    while True:
        try:
            r.ping()
            break
        except ConnectionError:
            log.info("Waiting start Redis")
            time.sleep(1)
    log.info("Redis connected")