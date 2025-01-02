from rest_framework import serializers
from .models import Post
from apps.categories.serializer import CategorySerializer
from apps.tags.serializer import TagSerializer
from apps.collections_.serializer import CollectionSerializer
from apps.profiles.serializer import ProfileSerializer
from tyf import settings


class PostSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()
    category = CategorySerializer()
    collections = CollectionSerializer(many=True)
    tags = TagSerializer(many=True)
    media = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    bookmarks = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        input_formats=[
            "%d.%m.%Y",
            "iso-8601",
        ],
    )
    updated_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        input_formats=[
            "%d.%m.%Y",
            "iso-8601",
        ],
    )
    filetypes = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_media(self, obj):
        media = obj.media.all()
        return media.count()

    def get_comments(self, obj):
        comments = obj.comments.all()
        return comments.count()

    def get_bookmarks(self, obj):
        bookmarks = obj.bookmarks.all()
        return bookmarks.count()

    def get_filetypes(self, obj):
        return obj.get_filetypes

    def get_thumbnail(self, obj):
        if obj.thumbnail:
            return settings.API_ULR + obj.thumbnail.url
        return None
