from .models import Post
from rest_framework import status
from rest_framework import viewsets
from .pagination import PostPagination
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializer import PostDetailSerializer, PostListSerializer


class PostViewSet(viewsets.ViewSet):
    pagination_class = PostPagination

    def list(self, _):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = PostListSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def retrieve(self, _, pk=None):
        queryset = Post.objects.all().order_by("-created_at")
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

    def get_queryset(self):
        return Post.objects.all().order_by("-created_at")
