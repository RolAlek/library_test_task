from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter

from .views import BookViewset, SignUpView

router = SimpleRouter()
router.register("books", BookViewset)

auth_patterns = [
    path("token/", views.obtain_auth_token),
    path("signup/", SignUpView.as_view()),
]

urlpatterns = [
    path("", include(router.urls)),
    path('auth/', include(auth_patterns)),
]
