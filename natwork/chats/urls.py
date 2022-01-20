from django.urls import path
from . import views

app_name = 'chats'

urlpatterns = [
    path('', views.chats, name='chats'),
    path('<int:user_id>/', views.messages, name='messages'),
]
