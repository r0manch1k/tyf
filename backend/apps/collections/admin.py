from django.contrib import admin
from .models import Collection


class CollectionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "emoji",
    )

    list_filter = ("name",)

    search_fields = ("name",)

    class Meta:
        model = Collection


admin.site.register(Collection, CollectionAdmin)
