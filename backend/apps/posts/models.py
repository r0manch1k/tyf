import os
import markdown
from django.db import models
from functools import partial
from django.db.models import Value
from mdeditor.fields import MDTextField
from django_resized import ResizedImageField
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.indexes import GinIndex, BTreeIndex
from apps.utils.media_tools import generate_uuid, generate_media_path
from django.contrib.postgres.search import SearchVectorField, SearchVector


from apps.tags.models import Tag
from apps.media.models import Media
from apps.profiles.models import Profile

# from apps.comments.models import Comment
from apps.categories.models import Category
from apps.collections.models import Collection


class Post(models.Model):
    manager = models.Manager()

    class Meta:
        indexes = [
            GinIndex(fields=["full_search_vector"]),
            BTreeIndex(fields=["title"]),
            BTreeIndex(fields=["author"]),
            BTreeIndex(fields=["category"]),
            BTreeIndex(fields=["identifier"]),
        ]

    active = models.BooleanField(default=True)
    identifier = models.CharField(
        max_length=8, primary_key=False, editable=False, unique=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name="category",
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
    )
    collections = models.ManyToManyField(
        Collection,
        verbose_name="collections",
        related_name="posts",
        blank=True,
    )
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(verbose_name="title", max_length=255)
    content = MDTextField(verbose_name="content")
    description = models.TextField(verbose_name="Description")
    thumbnail = ResizedImageField(
        crop=["middle", "center"],
        size=[650, 350],
        quality=100,
        upload_to=partial(
            generate_media_path, key="identifier", remove_with_same_key=True
        ),
        force_format="WEBP",
        blank=True,
        null=True,
        verbose_name="Thumbnail",
    )
    stars = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(
        Tag, verbose_name="tags", related_name="posts", blank=True
    )
    media = GenericRelation(Media)

    full_search_vector = SearchVectorField(null=True)

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

        Post.manager.filter(pk=self.pk).update(
            full_search_vector=(
                SearchVector("content", weight="A")
                + SearchVector("title", weight="B")
                + SearchVector(Value(self.author.username), weight="C")
            )
        )

    @property
    def get_filetypes(self):
        return list(
            set("*." + os.path.splitext(x.file.url)[1][1:] for x in self.media.all())
        )[:3]

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
