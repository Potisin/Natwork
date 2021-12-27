from core.services.paginator import my_paginator
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post


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


def profile(request):
    author = request.user
    posts_by_author = Post.objects.filter(author=author.id).order_by('-pub_date')
    count_posts = posts_by_author.count()
    context = {'author': author,
               'page_obj': my_paginator(request, posts_by_author, 10),
               'count_posts': count_posts
               }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post_by_id = get_object_or_404(Post, pk=post_id)
    count_author_posts = Post.objects.filter(author=post_by_id.author).count()
    context = {'post_by_id': post_by_id,
               'count_author_posts': count_author_posts}
    return render(request, 'posts/post_detail.html', context)
