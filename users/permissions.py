from rest_framework.permissions import BasePermission, IsAuthenticated, \
    SAFE_METHODS


class IsOwnerProfileOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS and obj.user == request.user


class IsOwnerProfile(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or request.user.role == 'admin'
        )
