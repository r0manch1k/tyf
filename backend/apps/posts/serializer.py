from rest_framework import serializers
from .models import Post
from apps.categories.serializer import CategorySerializer
from apps.tags.serializer import TagSerializer
from apps.collections_.serializer import CollectionSerializer
from apps.profiles.serializer import ProfileSerializer


class PostSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()
    category = CategorySerializer()
    collections = CollectionSerializer(many=True)
    tags = TagSerializer(many=True)
    media = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    bookmarks = serializers.SerializerMethodField()

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
