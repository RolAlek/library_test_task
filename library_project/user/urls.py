from django.urls import include, path

from .views import CreateCustomUserView

app_name = "auth"

urlpatterns = [
    path("auth/", include("django.contrib.auth.urls")),
    path(
        "auth/registration/",
        CreateCustomUserView.as_view(),
        name="registration",
    ),
]
