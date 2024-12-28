from rest_framework import serializers
from .models import Profile
from tyf import settings


class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    telegram_alias = serializers.SerializerMethodField()
    vkontakte_alias = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = "__all__"

    def get_avatar(self, obj):
        return settings.API_ULR + obj.get_avatar

    def get_telegram_alias(self, obj):
        return obj.get_telegram

    def get_vkontakte_alias(self, obj):
        return obj.get_vkontakte
