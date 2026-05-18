from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'notify_type', 'target_role', 'created_at')
    search_fields = ('title', 'body', 'notify_type', 'target_role')