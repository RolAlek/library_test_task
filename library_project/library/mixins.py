from django.core.exceptions import PermissionDenied


class LibrarianRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_librarian):
            raise PermissionDenied("Только для библиотекаря!")
        return super().dispatch(request, *args, **kwargs)
