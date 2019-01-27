
import pickle
import threading
import traceback

import dnode
from django.utils.module_loading import import_string
from lazypage import DJ_VERSION
from lazypage.utils import get_store_client
from lazypage.settings import lazypage_settings


store_client = get_store_client(decode_responses=False)  # store_client.get return bytes
expired_seconds = lazypage_settings.EXPIRED_SECONDS


def default_instantiate_method(request_dict):

    request = dnode.DNode(request_dict)

    # ================ patch for request.user =================
    user = request.user

    if DJ_VERSION < '2':
        from django.utils.deprecation import CallableBool
        request.user.is_anonymous = CallableBool(user.is_anonymous)
        request.user.is_authenticated = CallableBool(user.is_authenticated)

    return request


def execute_lazy_view(page_id, view_path, view_class_path, request, instantiate_method_path, *args, **kwargs):

    try:
        if view_path:
            view = import_string(view_path)
        elif view_class_path:
            view = import_string(view_class_path).as_view()
        else:
            assert False, 'view_path and view_class_path both need at least one!'

        if instantiate_method_path:
            instantiate_method = import_string(instantiate_method_path)
        else:
            instantiate_method = default_instantiate_method

        request = instantiate_method(request)

        response = view(request, *args, **kwargs)
        try:
            response.render()
        except:
            pass

        s = pickle.dumps(response)

        # task should make sure finished in expired seconds, or the url will be destroyed and raise a error
        url = store_client.get(page_id + ':url').decode()
        store_client.setex(url + ':response', expired_seconds, s)

    except Exception as e:
        # error msg will store 7 days at least
        s = max(3600 * 24 * 7, expired_seconds)
        error_msg = traceback.format_exc()
        store_client.setex(page_id + ':error', s, error_msg)
        raise e


def async_execute_lazy_view(page_id, view_path, view_class_path, request, instantiate_method_path, *args, **kwargs):
    args = (page_id, view_path, view_class_path, request, instantiate_method_path) + args
    t = threading.Thread(target=execute_lazy_view, args=args, kwargs=kwargs)
    t.start()

