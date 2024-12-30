from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from .models import Media


class MediaInline(GenericStackedInline):
    model = Media
    extra = 1
    fields = ["file", "description"]


class MediaAdmin(admin.ModelAdmin):
    list_display = ["file", "description", "content_type", "object_id"]
    search_fields = ["caption", "description"]


admin.site.register(Media, MediaAdmin)
