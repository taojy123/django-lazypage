
default_app_config = "lazypage.apps.LazypageConfig"

VERSION = '0.3.13'

try:
    import django
    DJ_VERSION = '%s.%s.%s' % django.VERSION[:3]
except Exception as e:
    DJ_VERSION = '0.0.0'


