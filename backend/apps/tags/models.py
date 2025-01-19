from django.db import models
from apps.utils.mediaTools import generate_pastel_color


class Tag(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, unique=True)
    color = models.CharField(
        max_length=10, primary_key=False, editable=False, blank=True, null=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = "#" + self.name
        self.color = generate_pastel_color()
        super(Tag, self).save(*args, **kwargs)
