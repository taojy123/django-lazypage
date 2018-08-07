from .urls import urlpatterns

VERSION = '0.2.0'

default_app_config = "lazypage.apps.LazypageConfig"

def get_urls():
    return urlpatterns, 'lazypage', 'lazypage'

