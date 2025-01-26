import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.chats import routing as chats_routing
from apps.notifications import routing as notifications_routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tyf.settings")


@database_sync_to_async
def get_user(token_key):
    try:
        validated_token = JWTAuthentication().get_validated_token(token_key)
        user = JWTAuthentication().get_user(validated_token)
    except Exception:
        user = AnonymousUser()
    return user


class TokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        try:
            token_key = (
                dict((x.split("=") for x in scope["query_string"].decode().split("&")))
            ).get("token", None)
        except ValueError:
            token_key = None

        scope["user"] = await get_user(token_key)
        return await self.app(scope, receive, send)


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            TokenAuthMiddleware(
                URLRouter(
                    chats_routing.websocket_urlpatterns
                    + notifications_routing.websocket_urlpatterns
                )
            )
        ),
    }
)
