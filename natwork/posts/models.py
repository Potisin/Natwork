from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    objects = None
    text = models.TextField()
    pub_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    #group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='posts', blank=True, null=True)

