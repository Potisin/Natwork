from django.urls import path


from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('new', views.new_post, name='new_post'),
    path('profile/<slug:username>/', views.profile, name='profile'),
    path('posts/<int:post_id>', views.post_detail, name='post_detail'),
    path('edit/<int:post_id>', views.edit_post, name='edit_post'),

]
