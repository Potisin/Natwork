from django.shortcuts import render, get_object_or_404

from .models import Publik
from posts.models import Post


def publik_post(request, slug):

    publik = get_object_or_404(Publik, slug=slug)
    posts = Post.object.filter(publik=publik).order_by('-pub_date')[:12]
    return render(request, 'publik.html', {'publik':publik, 'posts':posts})
