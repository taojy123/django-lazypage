
import pickle
import threading

import dnode
from django.utils.deprecation import CallableBool
from django.utils.module_loading import import_string
from lazypage.utils import get_store_client
from lazypage.settings import lazypage_settings


store_client = get_store_client(decode_responses=False)
expired_seconds = lazypage_settings.EXPIRED_SECONDS


def execute_lazy_view(page_id, view_path, view_class_path, request, *args, **kwargs):

    if view_path:
        view = import_string(view_path)
    elif view_class_path:
        view = import_string(view_class_path).as_view()
    else:
        assert False, 'view_path and view_class_path both need at least one!'

    request = dnode.DNode(request)

    # ================ patch for request.user =================
    user = request.user
    request.user.is_anonymous = CallableBool(user.is_anonymous)
    request.user.is_authenticated = CallableBool(user.is_authenticated)
    # =========================================================

    response = view(request, *args, **kwargs)
    try:
        response.render()
    except:
        pass

    s = pickle.dumps(response)

    # task should make sure finished in expired seconds, or the url will be destroyed and raise a error
    url = store_client.get(page_id + ':url').decode()
    store_client.setex(url + ':response', expired_seconds, s)


def async_execute_lazy_view(page_id, view_path, view_class_path, request, *args, **kwargs):
    args = (page_id, view_path, view_class_path, request) + args
    t = threading.Thread(target=execute_lazy_view, args=args, kwargs=kwargs)
    print(t, 'started')
    t.start()

