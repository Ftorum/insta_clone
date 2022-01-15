from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Post, PostFileContent
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NewPostForm
# from django.template import loader


# Create your views here.
class AllPostsListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'all_posts'
    template_name = 'all_posts.html'


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'index.html'

    def queryset(self):
        following = self.request.user.user_id.all().values_list('follower_id', flat=True)
        posts = self.model.objects.filter(
            user__in=following).order_by('-posted')
        return posts


class PostDetailedView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_detail.html'


@login_required
def NewPost(request):
    user = request.user
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            obj.likes = 0
            obj.save()
            return redirect('index')
    else:
        form = NewPostForm()

    context = {
        'form':form,
    }

    return render(request, 'newpost.html', context)
