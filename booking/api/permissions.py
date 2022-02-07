from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_customer:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_customer:
            return True
        else:
            return False
