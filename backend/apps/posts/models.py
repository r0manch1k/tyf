import os
import markdown
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from mdeditor.fields import MDTextField
from apps.utils.media_tools import generate_uuid

# from apps.comments.models import Comment
from apps.media.models import Media
from apps.profiles.models import Profile
from apps.categories.models import Category
from apps.collections_.models import Collection
from apps.tags.models import Tag


class Post(models.Model):
    active = models.BooleanField(default=True)
    identifier = models.CharField(
        max_length=8, primary_key=False, editable=False, unique=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="posts"
    )
    collections = models.ManyToManyField(Collection, related_name="posts", blank=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    content = MDTextField()
    stars = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)
    media = GenericRelation(Media)

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        **kwargs,
    ):
        md = markdown.Markdown(extensions=["fenced_code", "codehilite"])
        self.content = md.convert(self.content)
        self.identifier = generate_uuid(klass=Post)
        super(Post, self).save(force_insert, force_update, *args, **kwargs)

    @property
    def get_filetypes(self):
        return list(set(os.path.splitext(x.file.url)[1][1:] for x in self.media.all()))[
            :3
        ]

    def __str__(self):
        return self.title


class BookmarkPost(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="bookmarks"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="bookmarks")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} bookmarked {self.post} at {self.created_at}"
