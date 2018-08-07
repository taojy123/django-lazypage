
from django.conf import settings


USER_SETTINGS = getattr(settings, 'LAZYPAGE', None)


DEFAULTS = {
    'EXPIRED_SECONDS': 3600,
    'POLLING_SECONDS': 5,

    'ASYNC_BY_CELERY': False,
    'CELERY_BROKER_URL': 'redis://password@127.0.0.1:6379/1',

    'STORE_BY_REDIS': False,
    'REDIS_HOST': '127.0.0.1',
    'REDIS_PORT': '6379',
    'REDIS_PASSWORD': '',
    'REDIS_DB': '2',
}


class LazypageSettings(object):

    def __init__(self, user_settings=None, defaults=None):
        self.user_settings = user_settings or {}
        self.defaults = defaults or {}

    def __getattr__(self, attr):
        if attr not in self.defaults.keys():
            raise AttributeError('Invalid Lazypage setting: %r' % (attr))

        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]

        # Cache the result
        setattr(self, attr, val)
        return val


lazypage_settings = LazypageSettings(USER_SETTINGS, DEFAULTS)

