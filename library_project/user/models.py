import uuid
from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

from library.models import Book


class CustomUser(AbstractUser):
    LIBRARIAN = "librarian"
    READER = "reader"
    ROLES = [
        (LIBRARIAN, "Библиотекарь"),
        (READER, "Читатель"),
    ]
    first_name = models.CharField(max_length=32, null=True, blank=True)
    last_name = models.CharField(max_length=32, null=True, blank=True)
    role = models.CharField(choices=ROLES, max_length=32)
    staff_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        null=True,
        blank=True,
    )
    address = models.CharField(max_length=100, null=True, blank=True)

    def clean(self) -> None:
        if self.role == self.READER and not self.address:
            raise ValidationError(
                "`address` - обязательное поле для читателя."
            )
        if self.role == self.LIBRARIAN and not self.staff_id:
            raise ValidationError(
                "`staff_id` - обязательное поле для библиотекаря."
            )
        super().clean()

    def save(self, *args, **kwargs):
        if self.role == self.LIBRARIAN:
            self.address = None
        elif self.role == self.READER:
            self.staff_id = None
            self.is_staff = True
        self.clean()
        super().save(*args, **kwargs)

    @property
    def is_librarian(self) -> bool:
        return self.role == self.LIBRARIAN

    @property
    def is_reader(self) -> bool:
        return self.role == self.READER

    def __str__(self) -> str:
        return self.username


class UserBook(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="books",
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reader",
    )
    receiving_date = models.DateField(auto_now_add=True)

    @property
    def days_on_hands(self):
        return (date.today() - self.receiving_date).days
