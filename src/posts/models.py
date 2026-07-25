from django.db import models
from django.utils import timezone
from django.urls import reverse
from users.models import Author
from taggit.managers import TaggableManager

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("post_list_by_category", args=[self.slug])

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

class PostQuerySet(models.QuerySet):

    def published(self):
        return self.filter(status=Post.Status.PUBLISHED)

    def drafts(self):
        return self.filter(status=Post.Status.DRAFT)

    def archived(self):
        return self.filter(status=Post.Status.ARCHIVED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED = 'archived', 'Archived'
    title = models.CharField(max_length=250)
    tags = TaggableManager(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
    )
    slug = models.SlugField(unique=True, max_length=250)
    content = models.TextField()
    meta_description = models.CharField(max_length=160, blank=True)
    image = models.ImageField(upload_to='posts/%Y/%m/%d/', blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=Status.choices, default='draft')
    objects = PostQuerySet.as_manager()
    reading_time = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)

    def get_absolute_url(self):
        if not self.published_at:
            return '/' 
        return reverse(
            "post_detail",
            args=[
                self.published_at.year,
                self.published_at.month,
                self.published_at.day,
                self.slug,
            ],
        )

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'post'
        verbose_name_plural = 'posts'
    
