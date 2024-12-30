from django.contrib import admin
from .models import Comment
from apps.media.admin import MediaInline


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


class CommentAdmin(admin.ModelAdmin):
    inlines = [MediaInline]

    list_display = (
        "id",
        "content",
        "author",
        "created_at",
    )


admin.site.register(Comment, CommentAdmin)
