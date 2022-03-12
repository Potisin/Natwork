from django.urls import path

from follows import views as v
from . import views


app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_post, name='new_post'),
    path('profile/<slug:username>/', views.profile, name='profile'),
    path('post/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:post_id>/edit', views.edit_post, name='edit_post'),
    path('new_comment/<int:post_id>', views.NewCommentView.as_view(), name='new_comment'),
    path('follow/', v.follow_index, name='follow_index'),
    path('follow/<slug:username>/', v.profile_follow, name='follow'),
    path('unfollow/<slug:username>/', v.profile_unfollow, name='unfollow'),

]
