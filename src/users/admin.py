from django.contrib import admin
from .models import Author
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'created_at')
    search_fields = ('username', 'email', 'phone')
    list_filter = ('created_at',)
    