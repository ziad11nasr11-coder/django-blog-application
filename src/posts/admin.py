from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'status', 'published_at', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'author__username']
    list_filter = ('status', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at', 'published_at')
    list_display_links = ('title', 'slug')
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'email', 'active', 'created_at')
    search_fields = ['content', 'name', 'email']
    list_filter = ('active', 'created_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    show_facets = admin.ShowFacets.ALWAYS

