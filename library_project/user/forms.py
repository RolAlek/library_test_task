from typing import Any

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=32,
        required=True,
        help_text="Укажите ваше имя",
        label="Имя",
    )
    last_name = forms.CharField(
        max_length=32,
        required=True,
        help_text="Укажите вашу фамилию",
        label="Фамилия",
    )
    address = forms.CharField(
        max_length=128,
        required=True,
        help_text="Укажите ваш адрес",
        label="Адрес",
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            UserCreationForm.Meta.fields
            + ("first_name", "last_name", "address")
        )

    def save(self, commit: bool = True) -> Any:
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.address = self.cleaned_data["address"]

        if commit:
            user.save()

        return user
