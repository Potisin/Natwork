from django.contrib.auth import get_user_model
from django.db import models
from publik.models import Publik

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    publik = models.ForeignKey(Publik, on_delete=models.CASCADE, blank=True, null=True, related_name='posts')

