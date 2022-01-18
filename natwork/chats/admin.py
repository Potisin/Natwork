from django.contrib import admin

from .models import Chat


class ChatAdmin(admin.ModelAdmin):
    list_display = ("pk",)


admin.site.register(Chat, ChatAdmin)


