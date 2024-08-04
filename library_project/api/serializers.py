from django.contrib.auth import get_user_model
from library.models import Book
from rest_framework import serializers

User = get_user_model()


class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    genre = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Book
        fields = ("title", "author", "genre")


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
