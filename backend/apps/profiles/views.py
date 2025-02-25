from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .serializers import ProfileDetailSerializer, ProfileListSerializer
from apps.posts.serializers import PostListSerializer
from apps.chats.serializers import ChatListSerializer
from .models import Profile
from apps.follows.models import Follow
from apps.chats.models import Chat
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class ProfileViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        queryset = Profile.objects.all()
        serializer = ProfileListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Profile.objects.all()
        profile = get_object_or_404(queryset, username=pk)
        serializer = ProfileDetailSerializer(profile, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["GET"], url_path="recent", url_name="recent")
    def recent_users(self, request):
        queryset = Profile.objects.all().order_by("-date_joined")[:5]
        serializer = ProfileListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["GET"],
        url_path="most-active",
        url_name="most-active",
        permission_classes=[],
        authentication_classes=[],
    )
    def most_active_users(self, request):
        queryset = Profile.objects.annotate(nposts=Count("posts")).order_by("-nposts")[
            :5
        ]
        serializer = ProfileListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["GET"], url_path="posts", url_name="posts")
    def posts(self, request, pk=None):
        queryset = Profile.objects.all()
        profile = get_object_or_404(queryset, username=pk)
        serializer = PostListSerializer(profile.posts, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["GET"],
        permission_classes=[IsAuthenticated],
        authentication_classes=[JWTAuthentication],
        url_path="followers",
        url_name="followers",
    )
    def followers(self, request, pk=None):
        queryset = Profile.objects.all()
        profile = get_object_or_404(queryset, username=pk)
        followers = [follow.follower for follow in profile.followers.all()]
        serializer = ProfileListSerializer(followers, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["GET"],
        permission_classes=[IsAuthenticated],
        authentication_classes=[JWTAuthentication],
        url_path="following",
        url_name="following",
    )
    def following(self, request, pk=None):
        queryset = Profile.objects.all()
        profile = get_object_or_404(queryset, username=pk)
        following = [follow.following for follow in profile.following.all()]
        serializer = ProfileListSerializer(following, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["GET"],
        url_path="me",
        url_name="me",
        permission_classes=[IsAuthenticated],
        authentication_classes=[JWTAuthentication],
    )
    def me(self, request):
        email = request.user
        queryset = Profile.objects.all()
        profile = get_object_or_404(queryset, email=email)
        serializer = ProfileDetailSerializer(profile)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["POST"],
        url_path="follow",
        url_name="follow",
        permission_classes=[IsAuthenticated],
        authentication_classes=[JWTAuthentication],
    )
    def follow(self, request, pk=None):
        if not request:
            return Response(
                {"detail": "You need to login to follow users."}, status=401
            )
        user_to_follow = get_object_or_404(Profile, username=pk)
        email = request.user
        request_user = get_object_or_404(Profile, email=email)
        if request_user == user_to_follow:
            return Response({"detail": "You cannot follow yourself."}, status=400)
        if request_user.following.filter(following=user_to_follow).exists():
            Follow.objects.filter(
                follower=request_user, following=user_to_follow
            ).delete()
            return Response({"detail": "Unfollowed successfully."})
        else:
            Follow.objects.create(follower=request_user, following=user_to_follow)
            return Response({"detail": "Followed successfully."})

    @action(detail=True, methods=["PATCH"], url_path="avatar", url_name="avatar")
    def avatar(self, request, pk=None):
        queryset = Profile.objects.all()
        profile = get_object_or_404(queryset, username=pk)
        profile.avatar = request.data.get("avatar")
        profile.save()
        serializer = ProfileDetailSerializer(profile)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        queryset = Profile.objects.all()
        profile = get_object_or_404(queryset, username=pk)
        serializer = ProfileDetailSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["GET"],
        url_path="chats",
        url_name="chats",
        permission_classes=[IsAuthenticated],
        authentication_classes=[JWTAuthentication],
    )
    def chats(self, request, pk=None):
        queryset = Profile.objects.all()
        profile = get_object_or_404(queryset, username=pk)
        chats = profile.chats.all()
        serializer = ChatListSerializer(chats, context={"request": request}, many=True)
        return Response(serializer.data)

    @chats.mapping.post
    def create_chat(self, request, pk=None):
        request_user = Profile.objects.get(email=request.user)
        recepient_user = Profile.objects.get(username=pk)
        chat = Chat.objects.create()
        chat.participants.add(request_user, recepient_user)
        chat.save()
        serializer = ChatListSerializer(chat, context={"request": request})
        return Response(serializer.data)
