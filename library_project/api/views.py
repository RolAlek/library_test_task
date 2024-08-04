from django.contrib.auth import get_user_model
from library.models import Book
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from user.models import UserBook

from .serializers import BookSerializer, UserBookSerializer, SignUpSerializer

User = get_user_model()


class BookViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(
        detail=True,
        methods=("post",),
        permission_classes=(IsAuthenticated,),
    )
    def take_book(self, request, pk=None):
        book = self.get_object()

        if UserBook.objects.filter(book=book).exists():
            return Response(
                {"message": "Книга уже выдана."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_book = UserBook.objects.create(user=request.user, book=book)
        user_book.save()
        serializer = BookSerializer(book)
        return Response(
            {"detail": "Вы успешно получили книгу.", "book": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=("post",),
        permission_classes=(IsAuthenticated,),
    )
    def return_book(
        self,
        request,
        pk=None,
        permission_classes=(IsAuthenticated,),
    ):
        book = self.get_object()
        user_book = UserBook.objects.filter(user=request.user, book=book)
        if not user_book.exists():
            return Response(
                {"message": "Книга не выдана и в наличии на полках."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_book.delete()
        serializer = BookSerializer(book)
        return Response(
            {"detail": "Вы успешно вернули книгу.", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=False,
        methods=("get",),
        permission_classes=(IsAuthenticated,),
    )
    def my_books(self, request):
        user_books = UserBook.objects.filter(user=request.user)
        if not user_books.exists():
            return Response(
                {"message": "Вы не получили не одной книги."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = UserBookSerializer(
            user_books,
            many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()
