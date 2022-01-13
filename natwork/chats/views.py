from django.shortcuts import render, redirect
from .forms import MessageForm
from posts.models import User
from . import models


def new_message(request, username):
    to_user = User.objects.get(username=username)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.from_user = request.user
            message.to_user = to_user.id
            message.save()
            return redirect(request.path)  # ну это не сработает конечно же, пофикси потом
        return render(request, 'new_message.html', {'form': form})
    form = MessageForm()
    return render(request, 'new_message.html', {'form': form})


# возможно хуйня с юзерами тоже не сработает, тогда попробуй объявить поля формы с аргументами лейбл и дизейбл.

def chats(request):
    chats_list = models.Chat.objects.filter(members__in=[request.user.id])
    return render(request, 'chats/chats_list.html', {'chats_list': chats_list, 'user_profile': request.user})
