from django.contrib import admin
from .models import Post, Comment
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']
    list_filter = ('created_at', 'updated_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at')
    search_fields = ['content']
    list_filter = ('created_at',)
