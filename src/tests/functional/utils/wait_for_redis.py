import logging.config
import time

import backoff
from redis import Redis
from redis.exceptions import ConnectionError

from core.logger import LOGGING
from tests.functional.settings import TestSettings

redis_host = TestSettings().redis_host
logging.config.dictConfig(LOGGING)
log = logging.getLogger('')


@backoff.on_exception(backoff.expo,
                      ConnectionError,
                      max_time=60)
def conn_redis():
    r = Redis(redis_host)
    r.ping()
    log.info("Redis connected")


if __name__ == '__main__':
    log.info("Waiting start Redis")
    conn_redis()
