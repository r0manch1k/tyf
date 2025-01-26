from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "created_at", "read")

    class Meta:
        model = Notification


admin.site.register(Notification, NotificationAdmin)
