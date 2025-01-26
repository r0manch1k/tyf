from django.apps import AppConfig


class PostsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.posts"

    def ready(self):
        # flake8: noqa
        from . import signals
