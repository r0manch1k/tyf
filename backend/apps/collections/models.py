from django.db import models
from django.utils.text import slugify


class Collection(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, unique=True)
    description = models.TextField(blank=True)
    emoji = models.CharField(max_length=2, blank=True, null=True)
    slug = models.SlugField(default="", max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
