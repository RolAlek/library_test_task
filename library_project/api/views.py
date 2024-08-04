from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

from library.models import Book
from .serializers import BookSerializer, SignUpSerializer


User = get_user_model()

class BookViewset(ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()
