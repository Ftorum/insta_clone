from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Post, PostFileContent, Like
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NewPostForm
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
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


class PostDetailedView(TemplateView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, pk, **kwargs):
        context = super(PostDetailedView, self).get_context_data(**kwargs)
        context['post'] = Post.objects.get(id=pk)
        context['all_likes'] = Like.objects.filter(post=context['post']).all().count()
        context['user_like'] = Like.objects.filter(
            user=self.request.user, post=context['post']).exists()
        print('all_likes: ',context['all_likes'],' personal_like%:', context['user_like'])
        return context


def likes(request, option, id):
    post_now = Post.objects.get(id=id)
    print(post_now)
    try:
        if int(option) == 0:
            Like.objects.get(user=request.user,
                                  post=post_now).delete()
        else:
            new_f = Like(user=request.user, post=post_now)
            new_f.save()
        return HttpResponseRedirect(reverse('post_detail', args=[str(id)]))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('post_detail', args=[str(id)]))


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
