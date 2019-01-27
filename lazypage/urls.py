
from django.conf.urls import url
from lazypage.views import loading
from lazypage import DJ_VERSION


assert DJ_VERSION >= '1.9.0', 'Sorry, django-lazypage currently only support django between 1.9 and 1.11 versions!'


urlpatterns = [
    url(r'^loading/(?P<page_id>[\w\d]+?)/$', loading, name='loading'),
]


def get_urls():
    return urlpatterns, 'lazypage', 'lazypage'
