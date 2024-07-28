from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("user.urls")),
    path("library/", include("library.urls")),
]
