from django.urls import path
from blog.apps import BlogConfig
from blog.views import PostCreateView, PostListView, PostDetailView, PostUpdateView, PostDeleteView, toggle_activity

app_name = BlogConfig.name

urlpatterns = [
    path('post_create/', PostCreateView.as_view(), name="post_create"),
    path('', PostListView.as_view(), name="post_list"),
    path('post/<int:pk>/detail/', PostDetailView.as_view(), name="post_detail"),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name="post_edit"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post_delete"),
    path('blog_publish/<int:pk>/', toggle_activity, name="toggle_activity"),
]
