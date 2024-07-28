import uuid

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class CustomUser(AbstractUser):
    LIBRARIAN = "librarian"
    READER = "reader"
    ROLES = [
        (LIBRARIAN, "Библиотекарь"),
        (READER, "Читатель"),
    ]
    role = models.CharField(choices=ROLES, max_length=32)
    staff_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        null=True,
        blank=True,
    )
    address = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.username

    def clean(self) -> None:
        if self.role == self.READER and not self.address:
            raise ValidationError("`address` - обязательное поле для читателя.")
        if self.role == self.LIBRARIAN and not self.staff_id:
            raise ValidationError("`staff_id` - обязательное поле для библиотекаря.")
        super().clean()

    def save(self, *args, **kwargs):
        if self.role == self.LIBRARIAN:
            self.address = None
        elif self.role == self.READER:
            self.staff_id = None
            self.is_staff = True
        self.clean()
        super().save(*args, **kwargs)
