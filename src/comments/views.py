from datetime import timedelta

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.db.models import Count

from posts.models import Post

from .forms import CommentForm
from .models import Comment
from .utils import get_client_ip


def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )

    if request.method == "POST":
        form = CommentForm(
            request.POST,
            user=request.user
        )

        if form.is_valid():

            ip = get_client_ip(request)

            ten_minutes_ago = timezone.now() - timedelta(
                minutes=10
            )

            recent_comments = Comment.objects.filter(
                ip_address=ip,
                created_at__gte=ten_minutes_ago
            ).count()

            if recent_comments >= 5:
                messages.error(
                    request,
                    "Too many comments. Please try again later."
                )

                return redirect(
                    post.get_absolute_url()
                )

            comment = form.save(commit=False)

            comment.post = post
            comment.ip_address = ip

            if request.user.is_authenticated:
                comment.author = request.user
                comment.name = request.user.username
                comment.email = request.user.email

            comment.save()

            messages.success(
                request,
                "Your comment has been submitted and is waiting for approval."
            )

            return redirect(
                post.get_absolute_url()
            )

    else:
        form = CommentForm(
            user=request.user
        )

    comments = post.comments.approved()

    post_tags_ids = post.tags.values_list(
        "id",
        flat=True
    )

    similar_posts = (
        Post.objects.published()
        .filter(tags__in=post_tags_ids)
        .exclude(id=post.id)
        .annotate(
            same_tags=Count("tags")
        )
        .order_by(
            "-same_tags",
            "-published_at"
        )[:4]
    )

    return render(
        request,
        "post/detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
            "similar_posts": similar_posts,
        }
    )