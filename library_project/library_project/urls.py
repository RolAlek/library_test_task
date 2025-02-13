from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("library.urls")),
    path("admin/", admin.site.urls),
    path("users/", include("user.urls")),
    path("api/", include("api.urls")),
]
