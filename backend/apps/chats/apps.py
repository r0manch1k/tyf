from django.apps import AppConfig


class ChatsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.chats"

    def ready(self):
        # flake8: noqa
        import apps.chats.signals
