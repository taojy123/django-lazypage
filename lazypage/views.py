
from django.http import HttpResponseRedirect
from django.shortcuts import render

from lazypage.settings import lazypage_settings
from lazypage.utils import get_redis_client


redisclient = get_redis_client(decode_responses=False)
expired_seconds = lazypage_settings.EXPIRED_SECONDS


def loading(request, page_id):
    url = redisclient.get(page_id + ':url')
    if url:
        url = url.decode()
        response = redisclient.get(url + ':response')
        assert response is not None, 'response cannot be None in this moment, please check!'
        if response:
            # page has loaded
            return HttpResponseRedirect(url)
        else:
            # page is loading
            ttl = redisclient.ttl(page_id + ':url')
            polling_seconds = lazypage_settings.POLLING_SECONDS

    return render(request, 'lazypage/loading.html', locals())
