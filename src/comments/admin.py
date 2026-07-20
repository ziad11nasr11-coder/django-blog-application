from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "post",
        "status",
        "created_at",
    )
    list_filter = (
        "status",
        "created_at",
    )
    search_fields = (
        "body",
        "author__username",
        "post__title",
    )
    ordering = ("-created_at",)
    autocomplete_fields = (
        "author",
        "post",
    )