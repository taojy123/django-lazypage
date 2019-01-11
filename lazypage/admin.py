from django.contrib import admin
from lazypage.models import LazyStore


@admin.register(LazyStore)
class LazyStoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'error_msg', 'created_at', 'expired_at', 'is_expired']
    fields = ['key', 'value', 'created_at', 'expired_at']
    readonly_fields = ['key', 'value', 'created_at']

# http://hostdomain.com/admin/lazypage/lazystore/?key__endswith=:error
# go this page to see the failed tasks



