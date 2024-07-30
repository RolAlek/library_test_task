from typing import Any

from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView

from user.models import UserBook
from .models import Book

User = get_user_model()


class IndexView(ListView):
    model = Book
    ordering = ("title",)
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        book_id = request.POST.get("book_id")
        book = get_object_or_404(Book, id=book_id)
        user = request.user
        if UserBook.objects.filter(user=user, book=book).exists():
            UserBook.objects.filter(user=user, book=book).delete()
            book.checked_out = False
        else:
            UserBook.objects.create(user=user, book=book)
            book.checked_out = True
        book.save()
        return redirect("library:index")


class ReaderBooksView(ListView):
    model = UserBook
    template_name = "reader_books.html"

    def get_queryset(self) -> QuerySet[Any]:
        return UserBook.objects.prefetch_related("book").filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        book_id = request.POST.get("book_id")
        book = get_object_or_404(Book, id=book_id)
        user = request.user
        if not UserBook.objects.filter(user=user, book=book).exists():
            raise Http404('Библиотекарь не нашел запись о том что вы взяли эту книгу.')
        UserBook.objects.filter(user=user, book=book).delete()
        return redirect("library:reader_books")
