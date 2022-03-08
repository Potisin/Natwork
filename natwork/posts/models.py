from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from public.models import Public

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    public = models.ForeignKey(Public, on_delete=models.CASCADE, blank=True, null=True, related_name='posts')
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'post_id': self.id})


class Comment(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name='comments')

    def __str__(self):
        return self.text
