from django.contrib import admin
from .models import Post, Comment

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
        list_display    = ['title', 'slug', 'author', 'publish', 'status']
        list_filter     = ['status', 'publish', 'created', 'author']
        # list_editable   = ['title', 'status']
        search_fields   = ['title', 'slug', 'author']
        ordering        = ('status', 'publish')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
        list_display    = ['name', 'email', 'post', 'created', 'active']
        list_filter     = ['created', 'updated', 'active']
        # list_editable   = ['title', 'status']
        search_fields   = ['name', 'email', 'body']
        ordering        = ('updated',)