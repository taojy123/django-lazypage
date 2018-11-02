
from django.utils.module_loading import import_string
from lazypage.settings import lazypage_settings

try:
    from celery import Celery
except ImportError as e:
    print('You should install celery. $pip install celery>=4.2.1')
    raise e


assert lazypage_settings.ASYNC_BY_CELERY, 'CELERY_APP of LAZYPAGE settings must be set'

celery_app = lazypage_settings.CELERY_APP
assert celery_app, 'CELERY_APP of LAZYPAGE settings must be set'

if isinstance(celery_app, str):
    celery_app = import_string(celery_app)
assert isinstance(celery_app, Celery), 'CELERY_APP of LAZYPAGE settings must be a Celery object'

# celery_app.autodiscover_tasks('tasks')

@celery_app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


# $celery worker -A project_name -l info
