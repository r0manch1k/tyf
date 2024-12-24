from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "username",
        "email",
        "first_name",
        "last_name",
        "university",
        "date_of_birth",
        "date_joined",
    )

    list_filter = (
        "username",
        "email",
        "date_of_birth",
        "date_joined",
        "major",
    )

    fieldsets = [
        (None, {"fields": ["user", "username", "email", "avatar", "date_joined"]}),
        (
            "Personal info",
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "middle_name",
                    "university",
                    "major",
                    "bio",
                    "date_of_birth",
                    "telegram",
                    "vkontakte",
                ]
            },
        ),
        ("Stats", {"fields": ["points", "awards"]}),
    ]

    search_fields = [
        "username",
        "first_name",
        "last_name",
        "major",
    ]

    ordering = [
        "username",
    ]

    autocomplete_fields = ["university", "major"]

    class Meta:
        model = Profile


admin.site.register(Profile, ProfileAdmin)
