from django.conf import settings
from django.db import models

from posts.models import Post


class CommentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="comments",
        null=True,
        blank=True,
    )
    body = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=CommentStatus.choices,
        default=CommentStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["post"]),
            models.Index(fields=["author"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        author = self.author.username if self.author else "Deleted User"
        return f"{author} on {self.post.title}"