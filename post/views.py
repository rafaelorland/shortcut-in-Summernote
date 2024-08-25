from django.shortcuts import render, get_object_or_404
from .models import Post

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    content_rendered = post.render_content()
    return render(request, 'post_detail.html', {'post': post, 'content_rendered': content_rendered})

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})