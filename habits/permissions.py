from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Дает разрешение владельцу объекта."""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
