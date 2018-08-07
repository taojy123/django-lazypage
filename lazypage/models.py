from django.db import models
from django.utils import timezone

from lazypage.settings import lazypage_settings


expired_seconds = lazypage_settings.EXPIRED_SECONDS


def generate_expired_at():
    return timezone.now() + timezone.timedelta(seconds=expired_seconds)


class LazyStore(models.Model):

    key = models.TextField(db_index=True)
    value = models.BinaryField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField(default=generate_expired_at)

    @property
    def is_expired(self):
        return timezone.now() > self.expired_at

    @property
    def ttl(self):
        seconds = (self.expired_at - timezone.now()).total_seconds()
        return int(seconds)

    def __str__(self):
        return self.key

    def __unicode__(self):
        return self.key
