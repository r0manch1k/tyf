import json

# from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.text import slugify

# from channels.db import database_sync_to_async


class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        print(self.user)
        if self.user.is_anonymous:
            await self.close()
        else:
            self.group_name = f"notifications_{slugify(self.user)}"
            print(self.group_name)
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
        else:
            await self.close()

    async def notifications_send_one(self, event):
        print("notify", event)
        await self.send(
            text_data=json.dumps(
                {
                    "kind": event["kind"],
                    "message": event["message"],
                }
            )
        )
