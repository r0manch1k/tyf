from rest_framework.response import Response
from rest_framework import viewsets
from django.db.models import Count
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from .serializer import PostDetailSerializer, PostListSerializer
from apps.comments.serializer import CommentSerializer
from .models import Post
from rest_framework.permissions import IsAuthenticated


class PostViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def list(self, request):
        queryset = Post.objects.all()
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, identifier=pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    def create(self, request):
        serializer = PostDetailSerializer(data=request.data)  # PostCreateSerializer?
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    @action(
        detail=False,
        methods=["GET"],
        url_path="most-commented",
        url_name="most-commented",
    )
    def most_commented(self, request):
        queryset = Post.objects.annotate(ncomments=Count("comments")).order_by(
            "-ncomments"
        )[:5]
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["GET"],
        url_path="most-bookmarked",
        url_name="most-bookmarked",
    )
    def most_bookmarked(self, request):
        queryset = Post.objects.annotate(nbookmarks=Count("bookmarks")).order_by(
            "-nbookmarks"
        )[:5]
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["POST"],
        url_path="comments",
        url_name="comments",
        permission_classes=[IsAuthenticated],
        authentication_classes=[JWTAuthentication],
    )
    def comment(self, request, pk=None):
        print(f"Request data: {request.data}")
        if not request:
            return Response({"detail": "You need to login to comment."}, status=401)

        post = get_object_or_404(Post, identifier=pk)
        serializer = CommentSerializer(
            data=request.data,
            context={"request": request},
        )
        if not serializer.is_valid():
            print(f"Invalid data: {serializer.errors}")  # Печатаем ошибки
            return Response(serializer.errors, status=400)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)
        return Response(serializer.data, status=201)
