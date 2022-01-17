from django.shortcuts import render, redirect, reverse
from .forms import MessageForm
from .models import Chat
from django.db.models import Count


def create_chat(request, user_id):
    chats = Chat.objects.filter(members__in=[request.user.id, user_id]).annotate(c=Count('members')).filter(c=2)
    if chats.count() == 0:
        chat = Chat.objects.create()
        chat.members.add(request.user)
        chat.members.add(user_id)
    else:
        chat = chats.first()
    return redirect(reverse('chats:messages', kwargs={'chat_id': chat.id}))


def chats(request):
    chats_list = Chat.objects.filter(members=request.user.id)
    return render(request, 'chats/chats_list.html', {'chats_list': chats_list, 'user_profile': request.user})

def messages(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    if request.method == 'POST':
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('chats:messages', kwargs={'chat_id': chat_id}))
    return render(request, 'chats/messages.html', {
        'user_profile': request.user,
        'chat': chat,
        'form': MessageForm()
        }
    )

