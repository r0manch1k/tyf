from rest_framework.response import Response
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# from rest_framework.permissions import AllowAny

# from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Chat
from .serializers import ChatSerializer


class ChatViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Chat.objects.all()
        serializer = ChatSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Chat.objects.all()
        chat = get_object_or_404(queryset, uuid=pk)
        serializer = ChatSerializer(chat, context={"request": request})
        return Response(serializer.data)
