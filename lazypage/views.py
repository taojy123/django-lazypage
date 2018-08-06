
from django.http import HttpResponseRedirect
from django.shortcuts import render

from lazypage.settings import lazypage_settings
from lazypage.utils import get_redis_client


redisclient = get_redis_client(decode_responses=False)
expired_seconds = lazypage_settings.EXPIRED_SECONDS


def loading(request, page_id):

    status = redisclient.get(page_id + ':status')
    if status:
        status = status.decode()
        url = redisclient.get(page_id + ':url').decode()
        if status == 'loading':
            ttl = redisclient.ttl(page_id + ':status')
            polling_seconds = lazypage_settings.POLLING_SECONDS
        elif status == 'loaded':
            url = url.replace('lazypage_id', 'old_lazypage_id')
            if '?' in url:
                url += '&'
            else:
                url += '?'
            url += 'lazypage_id=%s' % page_id
            redisclient.setex(page_id + ':url', expired_seconds, url)
            return HttpResponseRedirect(url)

    return render(request, 'lazypage/loading.html', locals())
