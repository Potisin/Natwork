import null as null
from django.contrib.auth import get_user_model
from django.db import models
from django.db.transaction import commit

from public.models import Public

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    public = models.ForeignKey(Public, on_delete=models.CASCADE, blank=True, null=True, related_name='posts')

    def __str__(self):
        return self.text

