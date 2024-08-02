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

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user_books = UserBook.objects.filter(
            user=self.request.user.id
        ).values_list(
            "book_id", flat=True
        )
        context["user_books"] = user_books
        return context

    def post(self, request, *args, **kwargs):
        book_id = request.POST.get("book_id")
        book = get_object_or_404(Book, id=book_id)
        user = request.user
        if UserBook.objects.filter(user=user, book=book).exists():
            UserBook.objects.filter(user=user, book=book).delete()
        else:
            UserBook.objects.create(user=user, book=book)
        book.save()
        return redirect("library:index")


class ReaderBooksView(ListView):
    model = UserBook
    template_name = "reader_books.html"
    ordering = ("book__title",)

    def get_queryset(self) -> QuerySet[Any]:
        return UserBook.objects.prefetch_related("book").filter(
            user=self.request.user
        )

    def post(self, request, *args, **kwargs):
        book_id = request.POST.get("book_id")
        book = get_object_or_404(Book, id=book_id)
        user = request.user
        if not UserBook.objects.filter(user=user, book=book).exists():
            raise Http404(
                "Библиотекарь не нашел запись о том что вы взяли эту книгу."
            )
        UserBook.objects.filter(user=user, book=book).delete()
        return redirect("library:reader_books")


class DebtListView(ListView):
    model = UserBook
    template_name = 'debt.html'

    def get_queryset(self) -> QuerySet[Any]:
        return UserBook.objects.select_related("book", 'user').all()
