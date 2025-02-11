from rest_framework.response import Response
from rest_framework import viewsets
from django.core import exceptions

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# from rest_framework.permissions import AllowAny

from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Chat, Message
from .serializers import ChatListSerializer, ChatDetailSerializer, MessageSerializer
from apps.profiles.models import Profile


class ChatViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Chat.objects.all()
        serializer = ChatListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Chat.objects.all()
        try:
            chat = get_object_or_404(queryset, uuid=pk)
        except exceptions.ValidationError:
            return Response(status=404)
        if chat.participants.filter(email=request.user).exists():
            serializer = ChatDetailSerializer(chat)
            return Response(serializer.data)
        return Response(status=403)

    @action(detail=True, methods=["GET"], url_path="messages", url_name="messages")
    def messages(self, request, pk=None):
        chat = get_object_or_404(Chat, uuid=pk)
        messages = chat.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    @messages.mapping.post
    def create_message(self, request, pk=None):
        chat = get_object_or_404(Chat, uuid=pk)
        author = Profile.objects.get(email=request.user)
        message = Message.objects.create(
            chat=chat, author=author, text=request.data["text"]
        )
        serializer = MessageSerializer(message)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        chat = get_object_or_404(Chat, uuid=pk)
        if chat.participants.filter(email=request.user).exists():
            chat.title = request.data.get("title", chat.title)
            chat.save()
            serializer = ChatDetailSerializer(chat)
            return Response(serializer.data)
        return Response(status=403)

    @action(detail=True, methods=["POST"], url_path="avatar", url_name="avatar")
    def avatar(self, request, pk=None):
        chat = get_object_or_404(Chat, uuid=pk)
        if chat.participants.filter(email=request.user).exists():
            chat.avatar = request.data["avatar"]
            chat.save()
            serializer = ChatDetailSerializer(chat)
            return Response(serializer.data)
        return Response(status=403)
