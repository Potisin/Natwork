from django.shortcuts import render, redirect, reverse
from .forms import MessageForm
from .models import Chat
from django.views.generic import TemplateView
from django.db.models import Count


class CreateChatView(TemplateView):
    def get(self, request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id]).annotate(c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
        else:
            chat = chats.first()
        return redirect(reverse('chats:messages', kwargs={'chat_id': chat.id}))

# def new_message(request, username):
#     to_user = User.objects.get(username=username)
#     if request.method == 'POST':
#         form = MessageForm(request.POST)
#         if form.is_valid():
#             message = form.save(commit=False)
#             message.from_user = request.user
#             message.to_user = to_user.id
#             message.save()
#             return redirect(request.path)  # ну это не сработает конечно же, пофикси потом
#         return render(request, 'new_message.html', {'form': form})
#     form = MessageForm()
#     return render(request, 'new_message.html', {'form': form})


# возможно хуйня с юзерами тоже не сработает, тогда попробуй объявить поля формы с аргументами лейбл и дизейбл.

def chats(request):
    chats_list = Chat.objects.filter(members__in=[request.user.id])
    return render(request, 'chats/chats_list.html', {'chats_list': chats_list, 'user_profile': request.user})

class MessagesView(TemplateView):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.messages.filter(is_readed=False).exclude(author=request.user).update(is_readed=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None

        return render(
            request,
            'chats/messages.html',
            {
                'user_profile': request.user,
                'chat': chat,
                'form': MessageForm()
            }
        )

    def post(self, request, chat_id):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat_id = chat_id
            message.author = request.user
            message.save()
        return redirect(reverse('chats:messages', kwargs={'chat_id': chat_id}))



