
from lazypage.execution import execute_lazy_view
from lazypage.lazy_celery import celery_app


@celery_app.task
def execute_lazy_task(page_id, view_path, view_class_path, request, *args, **kwargs):
    execute_lazy_view(page_id, view_path, view_class_path, request, *args, **kwargs)
    return True

