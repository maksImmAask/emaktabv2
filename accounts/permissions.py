from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminRole(BasePermission):
    message = "Только админ"

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsManagerOrAdmin(BasePermission):
    message = "Только менеджер или админ"

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ["admin", "manager"]
        )


class ReadOnlyOrAdminWrite(BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.role == "admin"