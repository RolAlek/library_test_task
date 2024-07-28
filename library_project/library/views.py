from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView

from .models import Book


class IndexView(ListView):
    model = Book
    ordering = ("title",)
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        book_id = request.POST.get("book_id")
        book = get_object_or_404(Book, id=book_id)
        if book.checked_out:
            book.checked_out = False
        else:
            book.checked_out = True
        book.save()
        return redirect("index")
