from django.urls import path
from . import views

app_name = 'chats'

urlpatterns = [
    path('', views.chats, name='chats'),
    path('create/<int:user_id>/', views.create_chat, name='create_chat'),
    path('<int:chat_id>/', views.messages, name='messages'),
]
