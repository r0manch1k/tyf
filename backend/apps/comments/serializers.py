from rest_framework import serializers
from .models import Comment
from apps.media.serializers import MediaSerializer


class FilterCommentSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super(FilterCommentSerializer, self).to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True)
    replies = RecursiveSerializer(many=True)
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
        list_serializer_class = FilterCommentSerializer
        fields = [
            "identifier",
            "content",
            "stars",
            "created_at",
            "updated_at",
            "active",
            "media",
            "post",
            "author",
            "parent",
            "replies",
        ]
