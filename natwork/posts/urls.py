from django.urls import path


from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new_post, name='new_post'),
    path('profile/<slug:username>/', views.profile, name='profile'),
    path('post/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:post_id>/edit', views.edit_post, name='edit_post'),
    path('new_comment/<int:post_id>', views.NewCommentView.as_view(), name='new_comment'),

]
