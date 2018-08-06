
# # set the default Django settings module for the 'celery' program.
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

from __future__ import absolute_import
from celery import Celery, platforms
from lazypage.settings import lazypage_settings


platforms.C_FORCE_ROOT = True

broker = lazypage_settings.CELERY_BROKER_URL
celery_app = Celery('lazypage', broker=broker)

celery_app.autodiscover_tasks()


@celery_app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

