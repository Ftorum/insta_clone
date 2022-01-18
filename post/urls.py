from django.urls import path
from post.views import PostListView, PostDetailedView, AllPostsListView, likes
from .views import NewPost


urlpatterns = [
   	path('', PostListView.as_view(), name='index'),
	path('posts/', AllPostsListView.as_view(), name='all_posts'),
	path('<uuid:pk>',PostDetailedView.as_view(), name='post_detail'),
	path('newpost/', NewPost, name='newpost'),
	path('likes/<option>/<uuid:id>', likes, name='likes'),
]