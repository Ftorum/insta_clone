from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from authy.forms import SignupForm, ChangePasswordForm, EditProfileForm
from django.contrib.auth.models import User
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from authy.models import Profile
from django.template import loader
from django.http import HttpResponse

from django.core.paginator import Paginator

from .models import Profile
from django.views.generic import TemplateView
from post.models import Followers

# Create your views here.


def UserProfile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    articles = profile.favorites.all()

    # Pagination
    paginator = Paginator(articles, 6)
    page_number = request.GET.get('page')
    articles_paginator = paginator.get_page(page_number)

    template = loader.get_template('profile.html')

    context = {
        'articles': articles_paginator,
        'profile': profile,
    }

    return HttpResponse(template.render(context, request))


def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(
                username=username, email=email, password=password)
            return redirect('index')
    else:
        form = SignupForm()

    context = {
        'form': form,
    }

    return render(request, 'signup.html', context)


@login_required
def PasswordChange(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('change_password_done')
    else:
        form = ChangePasswordForm(instance=user)

    context = {
        'form': form,
    }

    return render(request, 'change_password.html', context)


def PasswordChangeDone(request):
    return render(request, 'change_password_done.html')


@login_required
def EditProfile(request):
    user = request.user.id
    profile = Profile.objects.get(user__id=user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile.picture = form.cleaned_data.get('picture')
            profile.first_name = form.cleaned_data.get('first_name')
            profile.last_name = form.cleaned_data.get('last_name')
            profile.location = form.cleaned_data.get('location')
            profile.url = form.cleaned_data.get('url')
            profile.profile_info = form.cleaned_data.get('profile_info')
            profile.save()
            return redirect('index')
    else:
        form = EditProfileForm()

    context = {
        'form': form,
    }

    return render(request, 'edit_profile.html', context)


class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=pk)
        context['follow_status'] = Followers.objects.filter(
            user_id=self.request.user, follower_id=context['profile'].user).exists()
        return context


def follow(request, username, option, id):
    following = get_object_or_404(User, username=username)
    print(following)
    try:
        f = Followers.objects.filter(
            user_id=request.user, follower_id=following).exists()

        if int(option) == 0 and f == True:
            Followers.objects.get(user_id=request.user,
                                  follower_id=following).delete()
        else:
            new_f = Followers(user_id=request.user, follower_id=following)
            new_f.save()
        return HttpResponseRedirect(reverse('profile', args=[str(id)]))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[str(id)]))


def validate(request):
    username = request.POST['username']
    data = {
        'taken' : User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

