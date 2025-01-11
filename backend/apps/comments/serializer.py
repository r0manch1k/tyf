from rest_framework import serializers
from .models import Comment
from apps.media.serializer import MediaSerializer


class CommentSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True)
    replies = serializers.SerializerMethodField()
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

    def get_replies(self, obj):
        return CommentSerializer(obj.replies.all(), many=True).data

    class Meta:
        model = Comment
        fields = ["identifier", "content", "stars", "created_at", "updated_at", "active", "media", "post", "author", "parent", "replies"]
