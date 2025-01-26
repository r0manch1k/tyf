from .models import Post
from rest_framework import status
from django.db.models import Count
from rest_framework import viewsets
from .pagination import PostPagination
from django.contrib.postgres.search import (
    SearchQuery,
    TrigramSimilarity,
)
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from apps.comments.serializer import CommentSerializer
from django.contrib.postgres.aggregates import StringAgg
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import PostDetailSerializer, PostListSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from .serializers import PostDetailSerializer, PostListSerializer
from apps.comments.serializers import CommentSerializer
from .models import Post
from rest_framework.permissions import IsAuthenticated


class PostViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    pagination_class = PostPagination

    def list(self, request):
        queryset = Post.manager
        query = request.query_params.get("query", "")
        searchMethod = request.query_params.get("search_method", None)

        if searchMethod:
            if searchMethod == "full":
                similarityVector = (
                    TrigramSimilarity("content", query, raw=True)
                    + TrigramSimilarity("title", query, raw=True)
                    + TrigramSimilarity("author__username", query, raw=True)
                )

                queryset = (
                    queryset.annotate(similarity=similarityVector)
                    .filter(similarity__gt=0.3)
                    .order_by("-similarity")
                ) or (
                    queryset.filter(full_search_vector=SearchQuery(query)).order_by(
                        "created_at"
                    )
                )

            elif searchMethod == "title":
                queryset = (
                    queryset.annotate(
                        similarity=TrigramSimilarity("title", query, raw=True)
                    )
                    .filter(similarity__gt=0.3)
                    .order_by("-similarity")
                )

            elif searchMethod == "author":
                queryset = (
                    queryset.annotate(
                        similarity=TrigramSimilarity(
                            "author__username", query, raw=True
                        )
                    )
                    .filter(similarity__gt=0.3)
                    .order_by("-similarity")
                )

            elif searchMethod == "tag":
                queryset = (
                    queryset.annotate(
                        tags_string=StringAgg("tags__name", delimiter=" ")
                    )
                    .annotate(similarity=TrigramSimilarity("tags_string", f"#{query}"))
                    .filter(similarity__gt=0.2)
                    .order_by("-similarity")
                )

            elif searchMethod == "category":
                queryset = (
                    queryset.annotate(
                        similarity=TrigramSimilarity("category__name", query, raw=True)
                    )
                    .filter(similarity__gt=0.2)
                    .order_by("-similarity")
                )

            elif searchMethod == "collection":
                queryset = (
                    queryset.annotate(
                        collections_string=StringAgg("collections__name", delimiter=" ")
                    )
                    .annotate(similarity=TrigramSimilarity("collections_string", query))
                    .filter(similarity__gt=0.2)
                    .order_by("-similarity")
                )

            else:
                return Response(
                    {"detail": "Поисковый метод не поддерживается."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        else:
            queryset = queryset.all().order_by("-created_at")

        page = self.paginate_queryset(queryset)
        serializer = PostListSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Post.manager.all().order_by("-created_at")
        post = get_object_or_404(queryset, identifier=pk)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    def create(self, request):
        serializer = PostDetailSerializer(data=request.data)
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
        queryset = Post.manager.annotate(ncomments=Count("comments")).order_by(
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
        queryset = Post.manager.annotate(nbookmarks=Count("bookmarks")).order_by(
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
