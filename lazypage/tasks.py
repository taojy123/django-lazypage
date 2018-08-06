
import pickle

import dnode
from django.utils.deprecation import CallableBool
from django.utils.module_loading import import_string
from lazypage.utils import get_redis_client
from lazypage.settings import lazypage_settings
from lazypage.celery import celery_app


redisclient = get_redis_client(decode_responses=False)


@celery_app.task(bind=True)
def execute_lazy_view(self, page_id, view_path, view_class_path, request, *args, **kwargs):

    if view_path:
        view = import_string(view_path)
    elif view_class_path:
        view = import_string(view_class_path).as_view()
    else:
        assert False, 'view_path and view_class_path both need at least one!'

    request = dnode.DNode(request)

    # ================ patch for request.user =================
    user = request.user
    request.user.is_anonymous = CallableBool(request.user.is_anonymous)
    request.user.is_authenticated = CallableBool(request.user.is_authenticated)
    # =========================================================

    response = view(request, *args, **kwargs)
    try:
        response.render()
    except:
        pass

    s = pickle.dumps(response)

    expired_seconds = lazypage_settings.EXPIRED_SECONDS
    redisclient.setex(page_id + ':response', expired_seconds, s)
    redisclient.setex(page_id + ':status', expired_seconds, 'loaded')
