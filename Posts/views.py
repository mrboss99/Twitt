from django.shortcuts import render
from .models import Post, Comment
from django.views.generic import ListView

class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = "posts"
    template_name = 'Posts/post/post_list.html'

