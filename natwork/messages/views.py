from django.shortcuts import render
from .forms import PrivateMessageForm


def new_message(request, username):
    to_user = User.objects.get(username=username)
    if request.method == 'POST':
        form = PrivateMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.from_user = request.user
            message.to_user = to_user.id
            meassage.save()
            return redirect(request.path) #ну это не сработает конечно же, пофикси потом
        return render(request, 'new_message.html', {'form': form})
    form = PrivateMessageForm()
    return render(request, 'new_message.html', {'form': form})

# возможно хуйня с юзерами тоже не сработает, тогда попробуй объявить поля формы с аргументами лейбл и дизейбл.
