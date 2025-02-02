from rest_framework import serializers
from apps.profiles.serializers import ProfileListSerializer
from .models import Chat, Message
from tyf import settings


class LastMessageField(serializers.Field):
    def get_attribute(self, instance):
        return instance

    def to_representation(self, value):
        last_message = value.messages.last()
        if last_message:
            return MessageSerializer(last_message).data
        return None


class ThumbnailField(serializers.Field):
    def get_attribute(self, instance):
        return instance

    def to_representation(self, value):
        if value:
            return settings.API_URL + value.thumbnail.url
        return None


class ChatListSerializer(serializers.ModelSerializer):
    participants = ProfileListSerializer(many=True)
    thumbnail = ThumbnailField()
    last_message = LastMessageField()
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Chat
        fields = (
            "id",
            "uuid",
            "name",
            "participants",
            "last_message",
            "thumbnail",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class ChatDetailSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()
    participants = ProfileListSerializer(many=True)
    thumbnail = ThumbnailField()

    class Meta:
        model = Chat
        fields = [
            "id",
            "uuid",
            "name",
            "participants",
            "thumbnail",
            "messages",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "created_at", "updated_at")

    def get_messages(self, obj):
        messages = obj.messages.all().order_by("created_at")
        return MessageSerializer(messages, many=True).data


class MessageSerializer(serializers.ModelSerializer):
    author = ProfileListSerializer()

    class Meta:
        model = Message
        fields = ["id", "author", "text", "created_at", "updated_at"]
        read_only_fields = ("id", "author", "created_at", "updated_at")
