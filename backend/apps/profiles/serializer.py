from rest_framework import serializers
from .models import Profile
from apps.registry.serializer import MajorListSerializer, UniversityListSerializer
from apps.tags.serializer import TagSerializer
from tyf import settings


class ProfileListSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        input_formats=[
            "%d.%m.%Y",
            "iso-8601",
        ],
    )
    points = serializers.IntegerField(read_only=True)
    posts_count = serializers.IntegerField(source="posts.count", read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "username", "avatar", "date_joined", "posts_count", "points"]

    def get_avatar(self, obj):
        return settings.API_ULR + obj.get_avatar


class ProfileDetailSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    telegram = serializers.URLField()
    vkontakte = serializers.URLField()
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
    major = MajorListSerializer()
    university = UniversityListSerializer()
    points = serializers.IntegerField(read_only=True)
    awards = serializers.IntegerField(read_only=True)
    tags = serializers.SerializerMethodField()
    is_following_request_user = serializers.SerializerMethodField()
    is_followed_by_request_user = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "avatar",
            "date_joined",
            "date_of_birth",
            "first_name",
            "last_name",
            "middle_name",
            "bio",
            "telegram_alias",
            "vkontakte_alias",
            "major",
            "university",
            "points",
            "awards",
            "telegram",
            "vkontakte",
            "tags",
            "is_following_request_user",
            "is_followed_by_request_user",
            "following_count",
            "followers_count",
            "posts_count",
        ]

    def get_avatar(self, obj):
        return settings.API_ULR + obj.get_avatar

    def get_telegram_alias(self, obj):
        return obj.get_telegram

    def get_vkontakte_alias(self, obj):
        return obj.get_vkontakte

    def get_is_following_request_user(self, obj):
        request = self.context.get("request", None)
        if request and request.user:
            email = request.user
            return obj.following.filter(following__email=email).exists()
        return False

    def get_is_followed_by_request_user(self, obj):
        request = self.context.get("request", None)
        if request and request.user:
            email = request.user
            return obj.followers.filter(follower__email=email).exists()
        return False

    # def get_following(self, obj):
    #     return ProfileListSerializer(obj.following.all(), many=True).data

    # def get_followers(self, obj):
    #     return ProfileListSerializer(obj.followers.all(), many=True).data

    def get_tags(self, obj):
        user_posts = obj.posts.all()
        tags = {}
        for post in user_posts:
            for tag in post.tags.all():
                if tag in tags:
                    tags[tag] += 1
                else:
                    tags[tag] = 1
        sorted_tags = sorted(tags.items(), key=lambda item: item[1], reverse=True)
        return TagSerializer([tag[0] for tag in sorted_tags], many=True).data

    def get_following_count(self, obj):
        return obj.following.count()

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_posts_count(self, obj):
        return obj.posts.count()
