import json as JSON
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .celery import app
from django.utils.text import slugify

# from rest_framework.renderers import JSONRenderer
from apps.notifications.serializers import NotificationSerializer
from apps.posts.models import Post
from apps.notifications.models import Notification
from apps.chats.models import Message
from apps.follows.models import Follow


@app.task
def send_new_post_notification(identifier):
    try:
        post = Post.objects.get(identifier=identifier)
        channel_layer = get_channel_layer()

        followers = [follow.follower for follow in post.author.followers.all()]
        for follower in followers:
            if follower != post.author:
                notification = Notification.objects.create(
                    recipient=follower,
                    kind="post",
                    target=post.identifier,
                    text=f"{post.author.username} опубликовал новый пост!",
                )

                json = JSON.dumps(NotificationSerializer(notification).data)

                print(f"Sending notification to {slugify(follower.email)}")
                async_to_sync(channel_layer.group_send)(
                    f"notifications_{slugify(follower.email)}",
                    {
                        "type": "notifications.send_one",
                        "json": json,
                    },
                )

    except Post.DoesNotExist:
        pass


@app.task
def send_new_message_notification(id):
    try:
        message = Message.objects.get(id=id)
        channel_layer = get_channel_layer()

        participants = message.chat.participants.all()
        for participant in participants:
            if participant != message.author:
                notification = Notification.objects.create(
                    recipient=participant,
                    kind="message",
                    target=message.chat.uuid,
                    text=f"{message.author.username} прислал вам сообщение!",
                )

                json = JSON.dumps(NotificationSerializer(notification).data)

                async_to_sync(channel_layer.group_send)(
                    f"notifications_{slugify(participant.email)}",
                    {
                        "type": "notifications.send_one",
                        "json": json,
                    },
                )
    except Message.DoesNotExist:
        pass


@app.task
def send_new_follower_notification(id):
    try:
        follow = Follow.objects.get(id=id)
        channel_layer = get_channel_layer()

        notification = Notification.objects.create(
            recipient=follow.following,
            kind="follower",
            target=follow.follower.username,
            text=f"{follow.follower.username} подписался на вас!",
        )

        json = JSON.dumps(NotificationSerializer(notification).data)

        async_to_sync(channel_layer.group_send)(
            f"notifications_{slugify(follow.following.email)}",
            {
                "type": "notifications.send_one",
                "json": json,
            },
        )
    except Follow.DoesNotExist:
        pass
