from django.contrib import admin

from .models import Author, Book, Genre

admin.register(Author)
admin.register(Book)
admin.register(Genre)
