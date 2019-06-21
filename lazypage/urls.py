
from lazypage.views import loading
from lazypage import DJ_VERSION


assert DJ_VERSION.split('.') >= ('1', '9'), 'Sorry, django-lazypage current only support django after than 1.9 versions! current is %s' % DJ_VERSION


if DJ_VERSION < '2':
	from django.conf.urls import url
else:
	from django.urls import re_path as url


urlpatterns = [
    url(r'^loading/(?P<page_id>[\w\d]+?)/$', loading, name='loading'),
]


def get_urls():
    return urlpatterns, 'lazypage', 'lazypage'
