from django.contrib import admin
from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "color",
    )

    list_filter = ("name",)

    search_fields = ("name",)

    class Meta:
        model = Tag


admin.site.register(Tag, TagAdmin)
