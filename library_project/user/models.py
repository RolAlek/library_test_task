import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    LIBRARIAN = 'librarian'
    READER ='reader'
    ROLES = [
        (LIBRARIAN, 'Библиотекарь'),
        (READER, 'Читатель'),
    ]
    role = models.CharField(choices=ROLES)

    def __str__(self) -> str:
        return self.username


class Librarian(CustomUser):
    staff_id = models.UUIDField(default=uuid.uuid4, editable=False)


class Reader(CustomUser):
    address = models.CharField(max_length=100)
