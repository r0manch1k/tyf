# import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.text import slugify


class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
        else:
            print(f"NotificationsConsumer - connect - {self.user}")
            self.group_name = f"notifications_{slugify(self.user)}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
        else:
            await self.close()

    async def notifications_send_one(self, event):
        json = event["json"]
        await self.send(text_data=json)
