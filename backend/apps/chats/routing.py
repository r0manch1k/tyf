from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chats/(?P<uuid>[0-9a-f-]+)/$", consumers.ChatsConsumer.as_asgi()),
]
