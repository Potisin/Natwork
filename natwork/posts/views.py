import username as username

from core.services.paginator import my_paginator
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post, User


def index(request):
    post_list = Post.objects.all().order_by('-pub_date')
    context = {'page_obj': my_paginator(request, post_list, 10)}
    return render(request, 'posts/index.html', context)


def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:index')

        return render(request, 'posts/new.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/new.html', {'form': form})


def profile(request, slug):
    author = get_object_or_404(User, slug=slug)
    # author = request.user
    posts_by_author = Post.objects.filter(user=author).order_by('-pub_date')
    count_posts = posts_by_author.count()
    context = {'author': author,
               'page_obj': my_paginator(request, posts_by_author, 10),
               'count_posts': count_posts
               }
    return render(request, 'posts/profile.html', context)


def post_detail(request):
    context = {}
    return render(request, 'posts/post_detail.html', context)
