from django.contrib import admin
from .models import Chat, Message


class MessageInline(admin.StackedInline):
    model = Message
    extra = 0


class MessageAdmin(admin.ModelAdmin):
    class Meta:
        model = Message

    list_display = ("id", "chat", "author", "text", "created_at", "updated_at")


class ChatAdmin(admin.ModelAdmin):
    inlines = [MessageInline]

    class Meta:
        model = Chat

    list_display = ("id", "uuid", "name", "created_at", "updated_at")


admin.site.register(Chat, ChatAdmin)
admin.site.register(Message, MessageAdmin)
