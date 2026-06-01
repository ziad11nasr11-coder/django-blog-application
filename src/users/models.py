from django.db import models
from django.contrib.auth.models import AbstractUser

class Author(AbstractUser):
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username