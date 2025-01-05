from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )

    list_filter = ("name",)

    search_fields = ("name",)

    class Meta:
        model = Category


admin.site.register(Category, CategoryAdmin)
