from django.contrib import admin

from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author", "publik")
    search_fields = ("text",)
    list_filter = ("pub_date",)


admin.site.register(Post, PostAdmin)
# Register your models here.

