from django import forms
from .models import PrivateMessage


class PrvateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        field = ('text',)