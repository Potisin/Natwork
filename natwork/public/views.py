from django.shortcuts import render, get_object_or_404

from .models import Public
from posts.models import Post


def public_post(request, slug):

    public = get_object_or_404(Public, slug=slug)
    posts = Post.objects.filter(public=public).order_by('-pub_date')
    return render(request, 'public.html', {'public': public, 'posts': posts})
