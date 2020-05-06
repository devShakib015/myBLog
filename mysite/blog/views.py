from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    return render(request, 'blog/index.html')

class PostListView(ListView):
    queryset = Post.objects.filter(status='published')
    paginate_by = 3
    context_object_name = 'p_p'
    template_name = 'blog/post_list.html'

def post_detail(request,posts):
    post = get_object_or_404(Post, slug=posts)
    context = {'post': post}
    return render(request, 'blog/post_detail.html', context)
