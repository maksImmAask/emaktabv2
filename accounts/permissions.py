from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsDirector(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "director"
        )


class IsTeacher(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "teacher"
        )


class IsStudent(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "student"
        )


class IsTeacherOrAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [
                "teacher",
                "admin",
            ]
        )


class IsDirectorOrAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [
                "director",
                "admin",
            ]
        )


class ReadOnlyOrAdmin(BasePermission):

    def has_permission(self, request, view):

        if (
            not request.user
            or not request.user.is_authenticated
        ):
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.role == "admin"
    
from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnlyTeacherOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.role in ["teacher", "admin"]