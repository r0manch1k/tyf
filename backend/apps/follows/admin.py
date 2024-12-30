from django.contrib import admin
from .models import Follow


class FollowAdmin(admin.ModelAdmin):
    list_display = [
        "follower",
        "following",
        "created_at",
    ]

    class Meta:
        model = Follow


admin.site.register(Follow, FollowAdmin)
