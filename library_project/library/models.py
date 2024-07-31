from django.db import models


class Author(models.Model):
    full_name = models.CharField(
        verbose_name="Автор",
        max_length=128,
        unique=True,
    )

    def __str__(self):
        return self.full_name


class Genre(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=128,
        unique=True,
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(
        verbose_name="Название",
        max_length=128,
        unique=True,
    )
    author = models.ForeignKey(
        Author,
        verbose_name="Автор",
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name="Жанр",
        on_delete=models.CASCADE,
    )
