
import re

from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.conf import settings

from lazypage.settings import lazypage_settings
from lazypage.utils import get_store_client


store_client = get_store_client(decode_responses=False)
expired_seconds = lazypage_settings.EXPIRED_SECONDS


def loading(request, page_id):

    url = store_client.get(page_id + ':url')
    if url:
        url = url.decode()
        origin_url = re.sub(r'[\&|\?]lazy_\w+$', '', url)
        response = store_client.get(url + ':response')
        assert response, 'response cannot be null in this moment, please check!'
    
        if len(response) == 6:
            # page is loading
            ttl = store_client.ttl(page_id + ':url')
            polling_seconds = lazypage_settings.POLLING_SECONDS
        else:
            # page has loaded
            return HttpResponseRedirect(url)

    error_msg = store_client.get(page_id + ':error')
    if error_msg:
        if settings.DEBUG:
            error_msg = error_msg.decode()
        else:
            error_msg = 'Lzay Task Failed!'

    return render(request, 'lazypage/loading.html', locals())
