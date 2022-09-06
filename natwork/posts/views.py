from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page
from core.services.paginator import my_paginator
from django.shortcuts import render, redirect, get_object_or_404
from follows.models import Follow
from .forms import PostForm, CommentForm
from .models import Post, User
from django.views.generic.base import View


# @cache_page(20)
def index(request):
    post_list = Post.objects.all().prefetch_related('author', 'public', 'comments')
    context = {'page_obj': my_paginator(request, post_list, 10)}
    return render(request, 'posts/index.html', context)


@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:index')
        return render(request, 'posts/new.html', {'form': form})

    form = PostForm()
    return render(request, 'posts/new.html', {'form': form})

dgs
@login_required
def edit_post(request, post_id):
    current_post = Post.objects.defer('pub_date').filter(pk=post_id).first()  # какая то херня чтобы не обновлять дату
    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES or None, instance=current_post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:index')
        return render(request, 'posts/new.html', {'form': form})
    form = PostForm(instance=current_post)
    return render(request, 'posts/new.html', {'form': form})


def profile(request, username):
    author = User.objects.get(username=username)
    posts_by_author = Post.objects.filter(author=author.id).order_by('-pub_date').prefetch_related('author', 'public',
                                                                                                   'comments')
    context = {'author': author,
               'page_obj': my_paginator(request, posts_by_author, 10)
               }
    if request.user.is_authenticated and Follow.objects.filter(user=request.user, author=author):
        context['following'] = True

    return render(request, 'posts/profile.html', context)


class PostDetailView(View):
    """ Страница с экземпляром поста """

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        return render(request, 'posts/post_detail.html', {'post': post})


class NewCommentView(LoginRequiredMixin, View):
    """Добавление нового комментария"""

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        form = CommentForm()
        return render(request, 'posts/new_comment.html', {'form': form,
                                                          'post': post})

    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('posts:post_detail', post_id)
        return render(request, 'posts/new_comment.html', {'form': form,
                                                          'post': post})
