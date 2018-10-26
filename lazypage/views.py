
from django.http import HttpResponseRedirect
from django.shortcuts import render

from lazypage.settings import lazypage_settings
from lazypage.utils import get_store_client


store_client = get_store_client(decode_responses=False)
expired_seconds = lazypage_settings.EXPIRED_SECONDS


def loading(request, page_id):
    url = store_client.get(page_id + ':url')
    if url:
        url = url.decode()
        response = store_client.get(url + ':response')
        assert response, 'response cannot be null in this moment, please check!'
    
        if len(response) == 6:
            # page is loading
            ttl = store_client.ttl(page_id + ':url')
            polling_seconds = lazypage_settings.POLLING_SECONDS
        else:
            # page has loaded
            return HttpResponseRedirect(url)

    return render(request, 'lazypage/loading.html', locals())
