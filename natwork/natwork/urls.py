from django.contrib import admin
from django.urls import include, path
from django.conf import settings


urlpatterns = [
    path('', include('posts.urls', namespace='posts')),
    path('auth/', include('users.urls', namespace='users')),
    path('auth/', include('django.contrib.auth.urls')),
    path('public/', include('public.urls')),
    path('admin/', admin.site.urls),
    path('about/', include('about.urls', namespace='about')),
    path('chats/', include('chats.urls', namespace='chats'))

]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)
