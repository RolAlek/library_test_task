from django.contrib.auth import get_user_model
from rest_framework import serializers

from library.models import Book
from user.models import UserBook

User = get_user_model()


class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    genre = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Book
        fields = ("title", "author", "genre")


class UserBookSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = UserBook
        fields = ("book", "receiving_date", "days_on_hands")


class SignUpSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate_username(self, value):
        if value is None or value.strip() == "":
            raise serializers.ValidationError("Username не может быть пустым.")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Пользователь с таким именем уже существует."
            )
        return value

    def validate(self, attrs):
        if (
            attrs["password"] in attrs["email"]
            or attrs["password"] in attrs["username"]
        ):
            raise serializers.ValidationError(
                "Пароль не может содержать имя пользователя или email"
            )
        return attrs

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "address",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
            "username": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "address": {"required": True},
        }
