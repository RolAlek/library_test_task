from django.urls import path

from .views import CreateCustomUserView

urlpatterns = [
    path(
        "registration/",
        CreateCustomUserView.as_view(),
        name="registration",
    ),
]
