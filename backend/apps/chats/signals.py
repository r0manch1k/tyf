from django.db.models.signals import post_save
from apps.celery_app.tasks import (
    send_new_message_notification as send_new_message_notification_task,
)
from .models import Message


def send_new_message_notification(sender, instance, created, **kwargs):
    if created:
        message = instance
        send_new_message_notification_task.delay(message.id)


post_save.connect(send_new_message_notification, sender=Message)
