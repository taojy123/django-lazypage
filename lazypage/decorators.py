import pickle
import re
import uuid

import easyserializer
from django.http import HttpResponseRedirect
from django.urls import reverse

from functools import wraps
from lazypage.utils import get_redis_client
from lazypage.settings import lazypage_settings
from lazypage.tasks import execute_lazy_view


redisclient = get_redis_client(decode_responses=False)


def lazypage_decorator(view):

    view_path = view_class_path = ''
    if hasattr(view, 'view_class'):
        view_class = view.view_class
        view_class_path = re.findall(r"class '(.+?)'", str(view_class))[0]
        print('load lazypage view_class_path:', view_class_path)
    else:
        view_path = view.__module__ + '.' + view.__name__
        print('load lazypage view_path:', view_path)

    def lazypage_view(request, *args, **kwargs):

        execute_by_task = kwargs.pop('execute_by_task', False)
        if execute_by_task:
            return view(request, *args, **kwargs)

        lazypage_id = request.GET.get('lazypage_id')
        if lazypage_id:
            s = redisclient.get(lazypage_id + ':response')
            if s:
                response = pickle.loads(s)
                return response
            else:
                url = reverse('lazypage:loading', kwargs={'page_id': lazypage_id})
                return HttpResponseRedirect(url)

        url = request.get_full_path()

        # ================ patch for request.user =================
        user = request.user
        is_anonymous = user.is_anonymous()
        is_authenticated = user.is_authenticated()
        # =========================================================

        request = easyserializer.serialize(request, limit_deep=4)

        # ================ patch for request.user =================
        request['user']['is_anonymous'] = is_anonymous
        request['user']['is_authenticated'] = is_authenticated
        # =========================================================

        expired_seconds = lazypage_settings.EXPIRED_SECONDS
        page_id = uuid.uuid4().hex
        redisclient.setex(page_id + ':status', expired_seconds, 'loading')
        redisclient.setex(page_id + ':response', expired_seconds, '')
        redisclient.setex(page_id + ':url', expired_seconds, url)

        kwargs['execute_by_task'] = True
        execute_lazy_view.delay(page_id, view_path, view_class_path, request, *args, **kwargs)

        url = reverse('lazypage:loading', kwargs={'page_id': page_id})
        return HttpResponseRedirect(url)

    # return lazypage_view
    return wraps(view)(lazypage_view)
