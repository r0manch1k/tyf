from rest_framework import serializers
from .models import Follow
from apps.profiles.serializers import ProfileListSerializer


class FollowSerializer(serializers.ModelSerializer):
    follower = ProfileListSerializer()
    following = ProfileListSerializer()
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        input_formats=[
            "%d.%m.%Y",
            "iso-8601",
        ],
    )

    class Meta:
        model = Follow
        fields = "__all__"
