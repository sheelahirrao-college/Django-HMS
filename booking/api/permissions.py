from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        else:
            return False


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_admin:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        else:
            return False


class IsStaff(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        else:
            return False
