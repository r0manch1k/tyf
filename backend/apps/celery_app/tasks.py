from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .celery import app
from django.utils.text import slugify
from apps.posts.models import Post
from apps.notifications.models import Notification
from apps.chats.models import Message


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
                    text=f"{post.author.username} опубликовал новый пост!",
                )

                print(f"Sending notification to {slugify(follower.email)}")
                async_to_sync(channel_layer.group_send)(
                    f"notifications_{slugify(follower.email)}",
                    {
                        "type": "notifications.send_one",
                        "kind": notification.kind,
                        "message": notification.text,
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
                    text=f"{message.author.username} прислал вам сообщение!",
                )

                async_to_sync(channel_layer.group_send)(
                    f"notifications_{slugify(participant.email)}",
                    {
                        "type": "notifications.send_one",
                        "kind": notification.kind,
                        "message": notification.text,
                    },
                )
    except Message.DoesNotExist:
        pass
