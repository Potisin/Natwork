from django.urls import path
from . import views

app_name = 'chats'

urlpatterns = [
    # path(),
    path('new_message', views.new_message, name='new_message'),
    path('', views.chats, name='chats'),
]
