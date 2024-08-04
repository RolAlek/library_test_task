from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Author, Book, Genre


class BookInline(admin.TabularInline):
    model = Book
    extra = 1


@admin.register(Book)
class BookAdmin(SimpleHistoryAdmin):
    list_display = ("title", "author", "genre")
    list_display_links = ("title",)
    search_fields = ("title",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = (BookInline,)
    list_display = ("full_name",)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    inlines = (BookInline,)
    list_display = ("name",)
