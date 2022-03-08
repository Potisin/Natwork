from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, reverse
from core.services.services import create_or_find_chat
from .forms import MessageForm
from .models import Chat


def chats(request):
    chat_list = Chat.objects.filter(members=request.user.id)
    return render(request, 'chats/chat_list.html', {'chat_list': chat_list})


@login_required
def messages(request, user_id):
    if user_id == request.user.id:
        return redirect('/')
    chat = create_or_find_chat(request, user_id)
    if request.method == 'POST':
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat.id
            message.author = request.user
            message.save()
        return redirect(reverse('chats:messages', kwargs={'user_id': user_id}))
    return render(request, 'chats/messages.html', {
        'chat': chat,
        'form': MessageForm()
    }
                  )
