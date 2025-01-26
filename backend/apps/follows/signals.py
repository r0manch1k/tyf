from django.db.models.signals import post_save
from apps.celery_app.tasks import (
    send_new_follower_notification as send_new_follower_notification_task,
)
from .models import Follow


def send_new_follower_notification(sender, instance, created, **kwargs):
    if created:
        follow = instance
        send_new_follower_notification_task.delay(follow.following.id)


post_save.connect(send_new_follower_notification, sender=Follow)
