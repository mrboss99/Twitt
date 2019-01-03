from django.contrib import admin
from Posts.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'date', 'status']
    list_filter = ['created']
