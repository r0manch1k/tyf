from .models import Post
from rest_framework import status
from rest_framework import viewsets
from .pagination import PostPagination
from django.contrib.postgres.search import (
    SearchQuery,
    TrigramSimilarity,
)
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.postgres.aggregates import StringAgg
from .serializer import PostDetailSerializer, PostListSerializer


class PostViewSet(viewsets.ViewSet):
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
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @property
    def paginator(self):
        if not hasattr(self, "_paginator"):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
