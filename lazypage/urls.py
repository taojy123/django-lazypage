
from django.conf.urls import url
from lazypage.views import loading


urlpatterns = [
    url(r'^loading/(?P<page_id>[\w\d]+?)/$', loading, name='loading'),
]


def get_urls():
    return urlpatterns, 'lazypage', 'lazypage'
