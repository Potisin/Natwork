from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class PrivateMessage(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return self.text
