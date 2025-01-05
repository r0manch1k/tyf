from rest_framework import serializers
from .models import Comment
from apps.media.serializer import MediaSerializer


class CommentSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True)
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        input_formats=[
            "%d.%m.%Y",
            "iso-8601",
        ],
    )
    update_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        input_formats=[
            "%d.%m.%Y",
            "iso-8601",
        ],
    )

    class Meta:
        model = Comment
        fields = "__all__"
