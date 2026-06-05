from django.db import models
from django.utils import timezone
from users.models import Author

class PostQuerySet(models.QuerySet):

    def published(self):
        return self.filter(status=Post.Status.PUBLISHED)

    def drafts(self):
        return self.filter(status=Post.Status.DRAFT)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'
    title = models.CharField(max_length=250)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    slug = models.SlugField(unique=True, max_length=250)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    views = models.IntegarField(default=0)
    likes = models.IntegarField(default=0)
    status = models.CharField(max_length=10, choices=Status.choices, default='draft')
    objects = PostQuerySet.as_manager()

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'post'
        verbose_name_plural = 'posts'
    
class CommentQuerySet(models.QuerySet):

    def approved(self):
        return self.filter(active=True)

    def pending(self):
        return self.filter(active=False)
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    objects = CommentQuerySet.as_manager()
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    class Meta:
        ordering = ['created_at']
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
    
