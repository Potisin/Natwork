from chats.models import Chat
from django.db.models import Count


def create_or_find_chat(request, user_id):
    chats = Chat.objects.filter(members__in=[request.user.id, user_id]).annotate(c=Count('members')).filter(c=2)
    if chats.count() == 0:
        chat = Chat.objects.create()
        chat.members.add(request.user)
        chat.members.add(user_id)
    else:
        chat = chats.first()
    return chat
