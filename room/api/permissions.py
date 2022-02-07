from rest_framework.permissions import BasePermission


class IsRoomManager(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_room_manager:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_room_manager:
            return True
        else:
            return False
        