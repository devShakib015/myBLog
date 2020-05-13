from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity


# Create your views here.
def index(request):
    return render(request, 'blog/index.html')

def post_list(request, tag_slug=None):
    posts = Post.objects.filter(status='published')
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, 4)
    page = request.GET.get('page')

    try:
        p_p = paginator.page(page)
    except PageNotAnInteger:
        p_p = paginator.page(1)
    except EmptyPage:
        p_p = paginator.page(paginator.num_pages)
    
    context = {
        'page': page,
        'p_p': p_p,
        'tag': tag
    }

    return render(request, 'blog/post_list.html', context)

def post_detail(request,posts):
    post = get_object_or_404(Post, slug=posts)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    # Lists of sismilar posts
    post_tags_id = post.tags.values_list('id', flat=True)
    published_posts = Post.objects.filter(status='published')
    similar_posts = published_posts.filter(tags__in=post_tags_id)\
                                    .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                    .order_by('-same_tags', '-publish')[:3]

    context = {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form, 'similar_posts': similar_posts}
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


def post_search(request):
    form = SearchForm()
    query = None
    results= []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_query = SearchQuery(query)
            search_vector = SearchVector('title', 'body')
            results = Post.objects.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=query).order_by('-rank')
        
    context = {
        'form': form,
        'query': query,
        'results': results
    }
    return render(request, 'blog/search.html', context)