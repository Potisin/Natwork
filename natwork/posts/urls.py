from django.urls import path

from users.urls import app_name
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('new', views.new_post, name='new_post')
]
