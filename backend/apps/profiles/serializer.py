from rest_framework import serializers
from .models import Profile
from tyf import settings


class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    telegram_alias = serializers.SerializerMethodField()
    vkontakte_alias = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        input_formats=[
            "%d.%m.%Y",
            "iso-8601",
        ],
    )
    date_of_birth = serializers.DateField(
        format="%Y-%m-%d",
        input_formats=[
            "%d.%m.%Y",
            "iso-8601",
        ],
    )

    class Meta:
        model = Profile
        fields = "__all__"

    def get_avatar(self, obj):
        return settings.API_ULR + obj.get_avatar

    def get_telegram_alias(self, obj):
        return obj.get_telegram

    def get_vkontakte_alias(self, obj):
        return obj.get_vkontakte
