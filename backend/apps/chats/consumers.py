import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat, Message
from .serializers import MessageSerializer
from apps.profiles.models import Profile


class ChatsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_name = self.scope["url_route"]["kwargs"]["chat_name"]
        self.chat_group_name = f"chat_{self.chat_name}"

        await self.channel_layer.group_add(self.chat_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender_username = text_data_json["sender"]

        sender = await self.get_user(sender_username)
        room = await self.get_chat(self.chat_name)
        message_obj = await self.create_message(room, sender, message)

        message_data = MessageSerializer(message_obj).data

        await self.channel_layer.group_send(
            self.chat_group_name,
            {"type": "chat_message", "message": message_data},
        )

        await self.channel_layer.group_send(
            "general_chats",
            {"type": "notify_new_message", "message": message_data},
        )

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def get_user(self, username):
        return Profile.objects.get(username=username)

    @database_sync_to_async
    def get_chat(self, room_name):
        return Chat.objects.get(name=room_name)

    @database_sync_to_async
    def create_message(self, room, sender, content):
        return Message.objects.create(room=room, sender=sender, content=content)
