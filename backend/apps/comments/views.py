from rest_framework.response import Response
from rest_framework import viewsets

# from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .serializers import CommentSerializer
from .models import Comment
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import status


class CommentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        queryset = Comment.objects.filter(parent=None)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Comment.objects.all()
        comment = get_object_or_404(queryset, identifier=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        comment = Comment.objects.get(identifier=pk)
        print(f"Comment author: {comment.author.id}")
        print(f"Request user: {request.user.profile.id}")
        if comment.author.id != request.user.profile.id:
            raise PermissionDenied("You can't delete this comment.")
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None):
        comment = Comment.objects.get(identifier=pk)
        if comment.author.id != request.user.profile.id:
            raise PermissionDenied("You can't update this comment.")
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
