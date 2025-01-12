from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .serializer import ProfileDetailSerializer, ProfileListSerializer
from apps.posts.serializer import PostListSerializer
from .models import Profile
from django.db.models import Count

# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.permissions import IsAuthenticated


class ProfileViewSet(viewsets.ViewSet):
    # TODO: example for permissions
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    # request.user -> is current user (by token)

    def list(self, request):
        queryset = Profile.objects.all()
        serializer = ProfileListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Profile.objects.all()
        profile = get_object_or_404(queryset, username=pk)
        serializer = ProfileDetailSerializer(profile)
        return Response(serializer.data)

    # TODO: recent_users or recent_profiles?
    @action(detail=False, methods=["GET"], url_path="recent", url_name="recent")
    def recent_users(self, request):
        queryset = Profile.objects.all().order_by("-date_joined")[:5]
        serializer = ProfileListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=False, methods=["GET"], url_path="most-active", url_name="most-active"
    )
    def most_active_users(self, request):
        queryset = Profile.objects.annotate(nposts=Count("posts")).order_by("-nposts")[
            :5
        ]
        serializer = ProfileListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["GET"], url_path="posts", url_name="posts")
    def user_posts(self, request, pk=None):
        queryset = Profile.objects.all()
        profile = get_object_or_404(queryset, username=pk)
        serializer = PostListSerializer(profile.posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["GET"], url_path="followers", url_name="followers")
    def followers(self, request, pk=None):
        queryset = Profile.objects.all()
        profile = get_object_or_404(queryset, username=pk)
        serializer = ProfileListSerializer(profile.followers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["GET"], url_path="following", url_name="following")
    def following(self, request, pk=None):
        queryset = Profile.objects.all()
        profile = get_object_or_404(queryset, username=pk)
        serializer = ProfileListSerializer(profile.following, many=True)
        return Response(serializer.data)
