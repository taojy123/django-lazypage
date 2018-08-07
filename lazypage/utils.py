
import redis
from lazypage.settings import lazypage_settings


def get_redis_client(decode_responses=True):
    assert lazypage_settings.STORE_BY_REDIS, 'must set STORE_BY_REDIS is True'

    host = lazypage_settings.REDIS_HOST
    port = lazypage_settings.REDIS_PORT
    password = lazypage_settings.REDIS_PASSWORD
    db = lazypage_settings.REDIS_DB
    return redis.StrictRedis(host=host, port=port, password=password, db=db, decode_responses=decode_responses)


def add_param_after_url(url, param):
    if '?' in url:
        url += '&'
    else:
        url += '?'
    url += param
    return url

