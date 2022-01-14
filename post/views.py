from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.template import loader


# Create your views here.

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'index.html'

    def queryset(self):
        following = self.request.user.follower.all().values_list('following', flat=True)
        return self.model.objects.filter(user__in = following).order_by('-posted')


class PostDetailedView(DetailView):
    model = Post
    ontext_object_name = 'post'
    template_name = 'post_detail.html'







        