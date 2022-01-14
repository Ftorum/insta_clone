from django.urls import path
from post.views import PostListView, PostDetailedView


urlpatterns = [
   	path('', PostListView.as_view(), name='index'),
	path('<uuid:pk>',PostDetailedView.as_view(), name='post_detail',)
]