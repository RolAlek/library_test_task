from django.contrib import admin

from .models import CustomUser, UserBook


@admin.register(UserBook)
class UserBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'is_returned')
    list_display_links = ('user', 'book')
    list_filter = ("is_returned",)

admin.site.register(CustomUser)
