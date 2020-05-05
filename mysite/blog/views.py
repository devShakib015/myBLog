from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.
def post_list(request):
    posts = Post.objects.all()
    published_posts = Post.objects.filter(status='published')
    context = {
        'posts': posts,
        'published_posts': published_posts,
    }
    return render(request, 'blog/index.html', context)

def post_detail(request,posts):
    post = get_object_or_404(Post, slug=posts)
    context = {'post': post}
    return render(request, 'blog/post_detail.html', context)
