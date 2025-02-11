from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat, Message
from apps.profiles.models import Profile


class ChatsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.uuid = self.scope["url_route"]["kwargs"]["uuid"]
        self.user = self.scope["user"]
        self.group_name = f"chat_{self.uuid}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.connect_user(self.uuid, self.user)
        await self.accept()

    async def disconnect(self, close_code):
        await self.disconnect_user(self.uuid, self.user)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def chat_send_message(self, event):
        json = event["json"]
        await self.send(text_data=json)

    @database_sync_to_async
    def get_user(self, username):
        return Profile.objects.get(username=username)

    @database_sync_to_async
    def get_chat(self, uuid):
        return Chat.objects.get(uuid=uuid)

    @database_sync_to_async
    def connect_user(self, uuid, user):
        chat = Chat.objects.get(uuid=uuid)
        chat.participants_online.add(user)
        chat.save()

    @database_sync_to_async
    def disconnect_user(self, uuid, user):
        chat = Chat.objects.get(uuid=uuid)
        chat.participants_online.remove(user)
        chat.save()

    @database_sync_to_async
    def create_message(self, chat, author, content):
        return Message.objects.create(chat=chat, author=author, content=content)
