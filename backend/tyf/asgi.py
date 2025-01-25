import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.chats import routing as chats_routing
from apps.notifications import routing as notifications_routing


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tyf.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                chats_routing.websocket_urlpatterns
                + notifications_routing.websocket_urlpatterns
            )
        ),
    }
)
