from rest_framework.response import Response
from rest_framework import viewsets
# from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .serializer import CommentSerializer
from .models import Comment


class CommentViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Comment.objects.filter(parent=None)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Comment.objects.all()
        comment = get_object_or_404(queryset, identifier=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
