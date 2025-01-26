from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    recipient = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(
        format="%d.%m.%Y в %H:%M",
        input_formats=[
            "%d.%m.%Y",
            "iso-8601",
        ],
    )

    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    def get_recipient(self, obj):
        return obj.recipient.username
