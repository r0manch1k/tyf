from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        email = request.user
        queryset = Notification.objects.filter(recipient__email=email)
        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        email = request.user
        queryset = Notification.objects.filter(recipient__email=email, read=False)
        notification = get_object_or_404(queryset, pk=pk)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["GET"],
        url_path="delete-read",
        url_name="delete-read",
    )
    def delete_read(self, request):
        email = request.user
        queryset = Notification.objects.filter(recipient__email=email, read=True)
        queryset.delete()
        return Response({"status": 200})

    @action(detail=False, methods=["GET"], url_path="unread", url_name="unread")
    def unread(self, request):
        email = request.user
        queryset = Notification.objects.filter(recipient__email=email, read=False)
        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["PUT"], url_path="read", url_name="read")
    def read(self, request, pk=None):
        notification = Notification.objects.get(pk=pk)
        notification.read = True
        notification.save()
        return Response({"status": 200})

    @action(detail=False, methods=["PUT"], url_path="read-all", url_name="read-all")
    def read_all(self, request):
        email = request.user
        queryset = Notification.objects.filter(recipient__email=email, read=False)
        for notification in queryset.all():
            notification.read = True
            notification.save()
        return Response({"status": 200})
