import os
from functools import partial
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from apps.utils.media_tools import generate_media_path
from django_prometheus.models import ExportModelOperationsMixin


class Media(ExportModelOperationsMixin("media"), models.Model):
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="media"
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    original_filename = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    file = models.FileField(
        upload_to=partial(
            generate_media_path, key="object_id", remove_with_same_key=False
        ),
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.original_filename and self.file:
            self.original_filename = os.path.basename(self.file.name)
        super(Media, self).save(*args, **kwargs)

    def filename(self):
        return os.path.basename(self.file.name)

    def filetype(self):
        return os.path.splitext(self.file.name)[1][1:]
