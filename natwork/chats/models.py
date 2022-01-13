from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Chat(models.Model):
    members = models.ManyToManyField(User, verbose_name='Участник')


class Message(models.Model):
    text = models.TextField()
    is_readed = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), related_name='sent_messages')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.text
