from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm

User = get_user_model()


class CreateCustomUserView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = "registration/registration_form.html"
    success_url = reverse_lazy("library:index")
