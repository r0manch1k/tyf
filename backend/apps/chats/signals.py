from django.db.models.signals import post_save
from apps.celery_app.tasks import (
    send_new_message_notification as send_new_message_notification_task,
    send_message_to_participants as send_message_to_participants_task,
)
from .models import Message, Chat


def send_new_chat_notification(sender, instance, created, **kwargs):
    if created:
        chat = instance
        participants = chat.participants.all()
        for participant in participants:
            participant.chats.add(chat)


def send_new_message_notification(sender, instance, created, **kwargs):
    if created:
        message = instance
        send_message_to_participants_task.delay(message.id)
        send_new_message_notification_task.delay(message.id)


post_save.connect(send_new_message_notification, sender=Message)
post_save.connect(send_new_chat_notification, sender=Chat)
