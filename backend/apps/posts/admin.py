from django.contrib import admin
from .models import Post, BookmarkPost
from apps.comments.admin import CommentInline
from apps.media.admin import MediaInline


class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline, MediaInline]

    list_display = [
        "title",
        "author",
        "category",
        "created_at",
        "updated_at",
        "active",
    ]

    list_filter = [
        "author",
        "category",
        "tags",
        "created_at",
        "updated_at",
    ]

    search_fields = [
        "title",
        "content",
        "author",
        "category",
        "tags",
    ]

    ordering = [
        "created_at",
        "updated_at",
    ]

    class Meta:
        model = Post


class BookmarkPostAdmin(admin.ModelAdmin):
    list_display = [
        "profile",
        "post",
        "created_at",
    ]

    class Meta:
        model = BookmarkPost


admin.site.register(Post, PostAdmin)
admin.site.register(BookmarkPost, BookmarkPostAdmin)
