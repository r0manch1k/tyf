from django.db.models.signals import post_save
from apps.celery_app.tasks import (
    send_new_post_notification as send_new_post_notification_task,
)
from .models import Post


def send_new_post_notification(sender, instance, created, **kwargs):
    if created:
        post = instance
        send_new_post_notification_task.delay(post.identifier)


post_save.connect(send_new_post_notification, sender=Post)
