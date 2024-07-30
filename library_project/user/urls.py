from django.urls import include, path

from .views import CreateCustomUserView

app_name = "auth"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path(
        "registration/",
        CreateCustomUserView.as_view(),
        name="registration",
    ),
]
