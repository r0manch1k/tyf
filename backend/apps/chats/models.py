import uuid
from functools import partial
from django.db import models
from django_resized import ResizedImageField
from django.core.files.base import ContentFile
from io import BytesIO
from apps.utils.media_tools import generate_media_path, generate_colored_image
from apps.profiles.models import Profile


class Chat(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255, default="Без названия")
    participants = models.ManyToManyField(Profile, related_name="chats")
    participants_online = models.ManyToManyField(
        Profile, related_name="chats_online", blank=True
    )
    thumbnail = ResizedImageField(
        crop=["middle", "center"],
        size=[650, 350],
        quality=100,
        upload_to=partial(generate_media_path, key="uuid", remove_with_same_key=True),
        force_format="WEBP",
        blank=True,
        null=True,
        verbose_name="Thumbnail",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        super().save(
            force_insert=force_insert, force_update=force_update, *args, **kwargs
        )
        if not self.thumbnail:
            self.generate_thumbnail()

    def generate_thumbnail(self):
        img = generate_colored_image()
        filename = f"{self.uuid}.webp"
        img_temp = BytesIO()
        img.save(img_temp, "WEBP")
        img_temp.seek(0)
        self.thumbnail.save(filename, ContentFile(img_temp.read()), save=True)
        img_temp.close()

    def __str__(self):
        return self.name


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="messages"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
