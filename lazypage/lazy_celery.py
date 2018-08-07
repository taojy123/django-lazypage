
# # set the default Django settings module for the 'celery' program.
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

try:
    from celery import Celery, platforms
except ImportError as e:
    print('You should install celery. $pip install celery>=4.2.1')
    raise e

from lazypage.settings import lazypage_settings


# platforms.C_FORCE_ROOT = True

broker = lazypage_settings.CELERY_BROKER_URL
celery_app = Celery('lazypage', broker=broker)

celery_app.autodiscover_tasks()


# $celery worker -A lazy_celery -l info


@celery_app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

