from rest_framework import serializers
from .models import Post, BookmarkPost
from apps.categories.serializer import CategorySerializer
from apps.media.serializer import MediaSerializer
from apps.comments.serializer import CommentSerializer
from apps.tags.serializer import TagSerializer
from apps.collections_.serializer import CollectionSerializer
from apps.profiles.serializer import ProfileListSerializer
from apps.categories.models import Category
from apps.media.models import Media
from apps.tags.models import Tag
from apps.collections_.models import Collection
from apps.utils.media_tools import generate_media_path

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
    tags = TagSerializer(
        many=True,
    )
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
        read_only_fields = [
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

    # def get_media(self, obj):
    #     media = obj.media.all()
    #     return media.count()

    # def get_comments(self, obj):
    #     comments = obj.comments.all()
    #     return comments.count()

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
    author = ProfileListSerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    collections = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all(), many=True, required=False
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, required=False
    )
    comments = CommentSerializer(many=True, read_only=True)
    bookmarks = BookmarkPostSerializer(many=True, read_only=True)
    media = serializers.PrimaryKeyRelatedField(
        queryset=Media.objects.all(), many=True, required=False
    )
    filetypes = serializers.SerializerMethodField()
    thumbnail = serializers.ImageField(required=False)
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        input_formats=["%d.%m.%Y", "iso-8601"],
        read_only=True,
    )
    updated_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        input_formats=["%d.%m.%Y", "iso-8601"],
        read_only=True,
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
        read_only_fields = ["created_at"]

    def get_filetypes(self, obj):
        return obj.get_filetypes

    def get_thumbnail(self, obj):
        if obj.thumbnail:
            return settings.API_ULR + obj.thumbnail.url  # why ULR?
        return None

    def create(self, validated_data):
        collections = validated_data.pop("collections", [])
        tags = validated_data.pop("tags", [])
        media = validated_data.pop("media", [])
        category = validated_data.pop("category", None)
        thumbnail = validated_data.pop("thumbnail", None)

        author = self.context["request"].user.profile

        post = Post.objects.create(author=author, category=category, **validated_data)

        if collections:
            post.collections.set(collections)

        if tags:
            post.tags.set(tags)

        if media:
            post.media.set(media)

        if thumbnail:
            post.thumbnail = thumbnail

        return post

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["category"] = CategorySerializer(instance.category).data
        data["collections"] = CollectionSerializer(
            instance.collections.all(), many=True
        ).data
        data["tags"] = TagSerializer(instance.tags.all(), many=True).data

        return data
