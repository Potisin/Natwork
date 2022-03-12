from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from core.services.paginator import my_paginator
from follows.models import Follow
from posts.models import Post, User


@login_required
def follow_index(request):
    following_list = Follow.objects.filter(user=request.user)
    author_list = []
    for f in following_list:
        author_list.append(f.author.id)
    post_list = Post.objects.filter(author__in=author_list).prefetch_related('author', 'public', 'comments')
    context = {'page_obj': my_paginator(request, post_list, 10)}
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    user = User.objects.get(username=username)
    Follow.objects.get_or_create(user=request.user, author=user)
    return redirect(reverse('posts:profile', kwargs={'username': username}))


@login_required
def profile_unfollow(request, username):
    user = User.objects.get(username=username)
    follow_record = Follow.objects.filter(user=request.user, author=user)
    follow_record.delete()
    return redirect(reverse('posts:profile', kwargs={'username': username}))
