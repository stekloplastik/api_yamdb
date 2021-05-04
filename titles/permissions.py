from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role == 'admin'
                or request.user.is_staff
                or request.user.is_superuser
            )
        if request.method in SAFE_METHODS:
            return True
