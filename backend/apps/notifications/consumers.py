from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class NotificationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if await self.get_is_anonymous():
            await self.close()
        else:
            self.group_name = f"notifications_{self.user.username}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def notifications_send_one(self, event):
        json = event["json"]
        await self.send(text_data=json)

    @database_sync_to_async
    def get_is_anonymous(self):
        return self.user.is_anonymous
