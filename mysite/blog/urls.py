from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.PostListView.as_view(), name='post_list'),
    path('<slug:posts>/', views.post_detail, name='post_detail')
]
