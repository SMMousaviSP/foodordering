from rest_framework import permissions

from service_api.models import Restaurant


class ManagerPermission(permissions.BasePermission):
    """
    Check if the user is a restaurant manager.
    """

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user.profile.is_manager


class HasRestaurant(permissions.BasePermission):
    """
    Check if the manager has created a restaurant to manage.
    """

    message = "You should create a restaurant first to be able to access it's foods"

    def has_permission(self, request, view):
        return bool(Restaurant.objects.filter(manager=request.user.pk).first())
