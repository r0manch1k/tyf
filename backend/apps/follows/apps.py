from django.apps import AppConfig


class FollowsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.follows"

    def ready(self):
        # flake8: noqa
        from . import signals
