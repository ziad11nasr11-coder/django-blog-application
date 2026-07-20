from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'name', 'email', 'status', 'created_at')
    search_fields = ['content', 'name', 'email']
    list_filter = ('status', 'created_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    show_facets = admin.ShowFacets.ALWAYS

