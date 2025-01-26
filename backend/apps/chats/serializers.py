from rest_framework import serializers
from apps.profiles.serializers import ProfileListSerializer
from .models import Chat, Message
from tyf import settings


class ChatListSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    participants = ProfileListSerializer(many=True)
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = (
            "id",
            "uuid",
            "name",
            "last_message",
            "participants",
            "thumbnail",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def get_last_message(self, obj):
        last_message = obj.messages.last()
        if last_message:
            return MessageSerializer(last_message).data
        return None

    def get_thumbnail(self, obj):
        profile = obj.participants.exclude(email=self.context["request"].user).first()
        return settings.API_ULR + profile.get_avatar


class ChatDetailSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()
    participants = ProfileListSerializer(many=True)

    class Meta:
        model = Chat
        fields = [
            "id",
            "uuid",
            "name",
            "participants",
            "messages",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "created_at", "updated_at")

    def get_messages(self, obj):
        messages = obj.messages.all().order_by("-created_at")
        return MessageSerializer(messages, many=True).data


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "author", "content", "created_at", "updated_at"]
        read_only_fields = ("id", "created_at", "updated_at")
