from django import template
from django.db.models import Count
from ..models import Post
from django.utils.safestring import mark_safe
import markdown
from ..forms import SearchForm


register = template.Library()

@register.simple_tag
def total_posts():
    published_posts = Post.objects.filter(status='published')
    return published_posts.count()

@register.simple_tag
def total_comments():
    total_comments = 0
    published_posts = Post.objects.filter(status='published')
    for post in published_posts:
        total_comments_in_post = post.comments.count()
        total_comments += total_comments_in_post
    return total_comments

@register.inclusion_tag('blog/latest_posts.html')
def show_latest_posts(count=5):
    published_posts = Post.objects.filter(status='published')
    l_t = published_posts.order_by('-publish')[:count]
    return {'l_t': l_t}

@register.inclusion_tag('blog/most_commented_posts.html')
def show_most_commented_posts(count=5):
    published_posts = Post.objects.filter(status='published')
    m_c_p = published_posts.annotate(t_c = Count('comments')).order_by('-t_c')[:count]
    return {'m_c_p': m_c_p}

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

@register.inclusion_tag('blog/search_form.html')
def show_search_form():
    form = SearchForm()
    return {'form': form}
