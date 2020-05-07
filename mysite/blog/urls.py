from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.PostListView.as_view(), name='post_list'),
    path('<slug:posts>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share')
]
