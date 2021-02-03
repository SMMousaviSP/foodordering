from rest_framework import permissions


class ManagerPermission(permissions.BasePermission):
    """
    Check if the user is a restaurant manager.
    """
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user.profile.is_manager
