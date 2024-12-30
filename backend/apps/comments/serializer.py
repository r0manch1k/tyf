from rest_framework import serializers
from .models import Comment
from apps.media.serializer import MediaSerializer


class CommentSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True)

    class Meta:
        model = Comment
        fields = "__all__"
