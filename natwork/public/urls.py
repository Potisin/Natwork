from django.urls import path

from . import views

urlpatterns = [path('<slug:slug>/', views.public_post, name='public')]
