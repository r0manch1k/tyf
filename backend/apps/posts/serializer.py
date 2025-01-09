from rest_framework import serializers
from .models import Post, BookmarkPost
from apps.categories.serializer import CategorySerializer
from apps.media.serializer import MediaSerializer
from apps.comments.serializer import CommentSerializer
from apps.tags.serializer import TagSerializer
from apps.collections_.serializer import CollectionSerializer
from apps.profiles.serializer import ProfileListSerializer
from tyf import settings


class BookmarkPostSerializer(serializers.ModelSerializer):
    profile = ProfileListSerializer()

    class Meta:
        model = BookmarkPost
        fields = ["id", "profile", "created_at"]


class PostListSerializer(serializers.ModelSerializer):
    author = ProfileListSerializer()
    category = CategorySerializer()
    collections = CollectionSerializer(many=True)
    tags = TagSerializer(many=True)
    bookmarks_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    filetypes = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
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

    class Meta:
        model = Post
        fields = [
            "id",
            "identifier",
            "title",
            "author",
            "category",
            "collections",
            "tags",
            "comments_count",
            "description",
            "bookmarks_count",
            "created_at",
            "updated_at",
            "filetypes",
            "thumbnail",
        ]

    def get_bookmarks_count(self, obj):
        bookmarks = obj.bookmarks.all()
        return bookmarks.count()

    def get_comments_count(self, obj):
        comments = obj.comments.all()
        return comments.count()

    def get_filetypes(self, obj):
        return obj.get_filetypes

    def get_thumbnail(self, obj):
        if obj.thumbnail:
            return settings.API_ULR + obj.thumbnail.url
        return None


class PostDetailSerializer(serializers.ModelSerializer):
    author = ProfileListSerializer()
    category = CategorySerializer()
    collections = CollectionSerializer(many=True)
    tags = TagSerializer(many=True)
    comments = CommentSerializer(many=True)
    bookmarks = BookmarkPostSerializer(many=True)
    media = MediaSerializer(many=True)
    filetypes = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()
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

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author",
            "category",
            "collections",
            "tags",
            "media",
            "comments",
            "bookmarks",
            "description",
            "created_at",
            "updated_at",
            "filetypes",
            "thumbnail",
        ]

    def get_filetypes(self, obj):
        return obj.get_filetypes

    def get_thumbnail(self, obj):
        if obj.thumbnail:
            return settings.API_ULR + obj.thumbnail.url
        return None
