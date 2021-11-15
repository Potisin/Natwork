from django.contrib import admin

from .models import Public


class PublikAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug')
    search_fields = ('slug',)


admin.site.register(Public, PublikAdmin)
