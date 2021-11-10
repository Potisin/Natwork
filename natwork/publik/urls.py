from django.urls import path

from . import views

urlpatterns = [path('<slug:slug>/', views.publik_post, name='publik')]
