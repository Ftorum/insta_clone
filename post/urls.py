from django.urls import path
from post.views import PostListView, PostDetailedView, AllPostsListView
from .views import NewPost


urlpatterns = [
   	path('', PostListView.as_view(), name='index'),
	path('posts/', AllPostsListView.as_view(), name='all_posts'),
	path('<uuid:pk>',PostDetailedView.as_view(), name='post_detail'),
	path('newpost/', NewPost, name='newpost'),
]