from django.db import models
from django.utils import timezone
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    #author = models.ForeignKey(Author, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=250)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'post'
        verbose_name_plural = 'posts'
    
    