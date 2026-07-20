from django.contrib import admin

from .models import Comment


@admin.action(description="Approve selected comments")
def approve_comments(modeladmin, request, queryset):
    queryset.update(
        status=Comment.Status.APPROVED
    )


@admin.action(description="Reject selected comments")
def reject_comments(modeladmin, request, queryset):
    queryset.update(
        status=Comment.Status.REJECTED
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "post",
        "name",
        "email",
        "status",
        "created_at",
    )

    search_fields = [
        "content",
        "name",
        "email",
        "post__title",
    ]

    list_filter = (
        "status",
        "created_at",
    )

    date_hierarchy = "created_at"

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    show_facets = admin.ShowFacets.ALWAYS

    actions = [
        approve_comments,
        reject_comments,
    ]