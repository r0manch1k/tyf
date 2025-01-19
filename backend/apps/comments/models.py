from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from mptt.models import MPTTModel, TreeForeignKey
from apps.profiles.models import Profile
from apps.posts.models import Post
from apps.media.models import Media
from apps.utils.mediaTools import generate_uuid


class Comment(MPTTModel):
    identifier = models.CharField(
        max_length=8, primary_key=False, editable=False, unique=True
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    media = GenericRelation(Media)
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    stars = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
        **kwargs,
    ):

        max_depth = 5
        if self.parent and self.parent.level >= max_depth - 1:
            self.parent = self.parent.parent
        self.identifier = generate_uuid(klass=Comment)
        super(Comment, self).save(force_insert, force_update, *args, **kwargs)
