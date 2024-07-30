from django.urls import path

from .views import IndexView, ReaderBooksView

app_name = "library"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("reader_books/", ReaderBooksView.as_view(), name="reader_books"),
]
