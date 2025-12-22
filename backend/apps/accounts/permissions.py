from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return obj.user == request.user


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
                request.user and
                request.user.is_authenticated and
                request.user.is_staff
        )