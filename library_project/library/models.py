from django.db import models
from simple_history.models import HistoricalRecords


class Author(models.Model):
    full_name = models.CharField(
        verbose_name="Автор",
        max_length=128,
        unique=True,
    )

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.full_name


class Genre(models.Model):
    name = models.CharField(
        verbose_name="Название",
        max_length=128,
        unique=True,
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

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
        related_name="books",
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name="Жанр",
        on_delete=models.CASCADE,
        related_name="books",
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self) -> str:
        return self.title
