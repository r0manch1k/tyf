import json as JSON
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .celery import app

from apps.notifications.serializers import NotificationSerializer
from apps.posts.models import Post
from apps.notifications.models import Notification
from apps.chats.models import Message
from apps.follows.models import Follow
from apps.profiles.models import Profile
from apps.chats.models import Chat
from apps.chats.serializers import MessageSerializer


# NOTIFICATIONS


def send_notification(notification: Notification, recepient: Profile):
    channel_layer = get_channel_layer()
    json = JSON.dumps(NotificationSerializer(notification).data)
    async_to_sync(channel_layer.group_send)(
        f"notifications_{recepient.username}",
        {
            "type": "notifications.send_one",
            "json": json,
        },
    )


@app.task
def send_new_post_notification(identifier):
    try:
        post = Post.objects.get(identifier=identifier)
        follows = post.author.followers.all()
        for follow in follows:
            notification = Notification.objects.create(
                recipient=follow.follower,
                kind="post",
                target=post.identifier,
                text=f"{post.author.username} опубликовал новый пост.",
            )
            send_notification(notification, follow.follower)
    except Post.DoesNotExist:
        pass


@app.task
def send_new_chat_notification(uuid):
    try:
        chat = Chat.objects.get(uuid=uuid)
        participants = chat.participants.all()
        for participant in participants:
            notification = Notification.objects.create(
                recipient=participant,
                kind="chat",
                target=chat.uuid,
                text=f"Новый чат с {', '.join([p.username for p in participants if p != participant])}.",
            )
            send_notification(notification, participant)
    except Chat.DoesNotExist:
        pass


@app.task
def send_new_message_notification(id):
    try:
        message = Message.objects.get(id=id)
        participants = message.chat.participants.all()

        participants_online = message.chat.participants_online.all()

        recipients = [
            participant
            for participant in participants
            if participant != message.author and participant not in participants_online
        ]

        for recipient in recipients:
            notification = Notification.objects.create(
                recipient=recipient,
                kind="message",
                target=message.chat.uuid,
                text=f"{message.author.username} прислал вам сообщение.",
            )
            send_notification(notification, recipient)
    except Message.DoesNotExist:
        pass


@app.task
def send_new_follower_notification(id):
    try:
        follow = Follow.objects.get(id=id)
        notification = Notification.objects.create(
            recipient=follow.following,
            kind="follower",
            target=follow.follower.username,
            text=f"{follow.follower.username} подписался на вас.",
        )
        send_notification(notification, follow.following)
    except Follow.DoesNotExist:
        pass


# CHATS


@app.task
def send_message_to_participants(id):
    try:
        message = Message.objects.get(id=id)
        chat = message.chat
        channel_layer = get_channel_layer()
        json = JSON.dumps(MessageSerializer(message).data)
        async_to_sync(channel_layer.group_send)(
            f"chat_{chat.uuid}",
            {
                "type": "chat.send_message",
                "json": json,
            },
        )

    except Message.DoesNotExist:
        pass
