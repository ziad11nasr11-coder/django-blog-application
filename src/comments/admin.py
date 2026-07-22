from django.contrib import admin
from django.contrib import messages
from .models import Comment


@admin.action(description="Approve selected comments")
def approve_comments(modeladmin, request, queryset):
    updated = queryset.update(status=Comment.Status.APPROVED)

    modeladmin.message_user(
        request,
        f"{updated} comment(s) approved successfully.",
        level=messages.SUCCESS,
    )


@admin.action(description="Reject selected comments")
def reject_comments(modeladmin, request, queryset):
    updated = queryset.update(status=Comment.Status.REJECTED)

    modeladmin.message_user(
        request,
        f"{updated} comment(s) rejected successfully.",
        level=messages.WARNING,
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