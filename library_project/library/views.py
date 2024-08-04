from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView

from user.models import UserBook

from .mixins import LibrarianRequiredMixin
from .models import Book

User = get_user_model()


class IndexView(ListView):
    model = Book
    ordering = ("title",)
    template_name = "index.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user_books = UserBook.objects.filter(
            user=self.request.user.id,
            returned_date=None,
        ).values_list("book_id", flat=True)
        context["user_books"] = user_books
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        book = get_object_or_404(Book, id=request.POST.get("book_id"))
        instance, created = UserBook.objects.get_or_create(
            user=user,
            book=book,
            returned_date=None,
        )
        if not created:
            instance.returned_date = timezone.now()
            instance.is_returned = True
        instance.save()
        return redirect("library:index")


class ReaderBooksView(LoginRequiredMixin, ListView):
    model = UserBook
    template_name = "reader_books.html"
    ordering = ("book__title",)

    def get_queryset(self) -> QuerySet[Any]:
        return UserBook.objects.prefetch_related("book").filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        instance = UserBook.objects.filter(
            user=request.user,
            book=get_object_or_404(Book, id=request.POST.get("book_id")),
            returned_date=None,
        )
        if not instance.exists():
            raise Http404(
                "Библиотекарь не нашел запись о том что вы взяли эту книгу."
            )
        instance = instance.first()
        instance.returned_date = timezone.now()
        instance.is_returned = True
        instance.save()
        return redirect("library:reader_books")


class DebtListView(LibrarianRequiredMixin, ListView):
    model = UserBook
    template_name = "debt.html"

    def get_queryset(self) -> QuerySet[Any]:
        return UserBook.objects.select_related("book", "user").all()
