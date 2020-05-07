from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm
from django.core.mail import send_mail


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

def post_share(request, post_id):
    # Retrieve post_id by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method =='POST':
        # A form was submitted.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # .....Send email
            post_url = request.build_absolute_uri('post.slug/')
            subject = '{} ({}) recommends your reading " {}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'kmshahriahhossain@gmail.com', [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    context = {
        'post': post, 'form': form, 'sent': sent
    }
    return render(request, 'blog/share.html', context)