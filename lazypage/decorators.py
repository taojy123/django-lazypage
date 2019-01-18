import pickle
import re
import uuid

import easyserializer
from django.http import HttpResponseRedirect
from django.urls import reverse

from functools import wraps

from lazypage.utils import get_store_client, add_param_after_url
from lazypage.settings import lazypage_settings


store_client = get_store_client(decode_responses=False)
expired_seconds = lazypage_settings.EXPIRED_SECONDS


def default_serialize_method(request):

    request_dict = easyserializer.serialize(request, limit_deep=4)

    # ================ patch for request.user =================
    user = request.user
    request_dict['user']['is_anonymous'] = user.is_anonymous()
    request_dict['user']['is_authenticated'] = user.is_authenticated()

    return request_dict


def lazypage_decorator(function=None, serialize_method=None, instantiate_method_path=None):

    if serialize_method is None:
        serialize_method = default_serialize_method

    def actual_decorator(view):

        view_path = view_class_path = ''
        if hasattr(view, 'view_class'):
            view_class = view.view_class
            view_class_path = re.findall(r"class '(.+?)'", str(view_class))[0]
        else:
            view_path = view.__module__ + '.' + view.__name__

        def lazypage_view(request, *args, **kwargs):

            execute_by_task = kwargs.pop('execute_by_task', False)
            if execute_by_task:
                return view(request, *args, **kwargs)

            # the params after `#`, will be ignored
            url = request.get_full_path()

            s = store_client.get(url + ':response')
            if s:

                # if the page is loading now, redirect to the loading page
                if len(s) == 6:
                    page_id = s.decode()
                    url = reverse('lazypage:loading', kwargs={'page_id': page_id})
                    return HttpResponseRedirect(url)

                # if the page has loaded, return the response
                response = pickle.loads(s)
                return response

            request = serialize_method(request)

            page_id = uuid.uuid4().hex[-6:]
            url = add_param_after_url(url, 'lazy_%s' % page_id)
            store_client.setex(page_id + ':url', expired_seconds, url)
            store_client.setex(url + ':response', expired_seconds, page_id)

            kwargs['execute_by_task'] = True

            if lazypage_settings.ASYNC_BY_CELERY:
                from lazypage.tasks import execute_lazy_task
                execute_lazy_task.delay(page_id, view_path, view_class_path, request, instantiate_method_path, *args, **kwargs)
            else:
                from lazypage.execution import async_execute_lazy_view
                async_execute_lazy_view(page_id, view_path, view_class_path, request, instantiate_method_path, *args, **kwargs)

            url = reverse('lazypage:loading', kwargs={'page_id': page_id})
            return HttpResponseRedirect(url)

        # return lazypage_view
        return wraps(view)(lazypage_view)

    if function:
        return actual_decorator(function)

    return actual_decorator
