

from lazypage.settings import lazypage_settings


class LazyStoreClient(object):

    def __init__(self, decode_responses=True):
        self.decode_responses = decode_responses

    def get(self, name):
        from lazypage.models import LazyStore
        store = LazyStore.objects.filter(key=name).first()
        if not store:
            return None
        if store.is_expired:
            store.delete()
            return None
        value = bytes(store.value)
        if self.decode_responses:
            try:
                value = value.decode()
            except:
                pass
        return value

    def setex(self, name, time, value):
        # expired seconds will be set by lazypage_settings, so here `time` just to be consistent with redis client.
        from lazypage.models import LazyStore
        try:
            value = value.encode()
        except:
            pass
        LazyStore.objects.filter(key=name).delete()
        LazyStore.objects.create(key=name, value=value)
        return value

    def ttl(self, name):
        from lazypage.models import LazyStore
        store = LazyStore.objects.filter(key=name).first()
        if not store:
            return 0
        return store.ttl


def get_redis_client(decode_responses=True):
    try:
        import redis
    except ImportError as e:
        print('You should install redis. $pip install redis>=2.10.6')
        raise e
    host = lazypage_settings.REDIS_HOST
    port = lazypage_settings.REDIS_PORT
    password = lazypage_settings.REDIS_PASSWORD
    db = lazypage_settings.REDIS_DB
    return redis.StrictRedis(host=host, port=port, password=password, db=db, decode_responses=decode_responses)


def get_store_client(decode_responses=True):
    if lazypage_settings.STORE_BY_REDIS:
        return get_redis_client(decode_responses)
    else:
        return LazyStoreClient(decode_responses)


def add_param_after_url(url, param):
    if '?' in url:
        url += '&'
    else:
        url += '?'
    url += param
    return url

