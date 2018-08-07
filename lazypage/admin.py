from django.contrib import admin
from lazypage.models import LazyStore


@admin.register(LazyStore)
class OverviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'created_at', 'expired_at', 'is_expired']

