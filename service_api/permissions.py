from rest_framework import permissions

from service_api.models import Restaurant, Food, Order


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


class IsFoodOwner(permissions.BasePermission):
    """
    Check if the manager is the owner of the food which wants to edit.
    """

    message = "You are not the owner of this food restaurant"

    def has_permission(self, request, view):
        food = Food.objects.filter(pk=view.kwargs.get("pk", None)).first()
        if food is None:
            return False
        return (
            Restaurant.objects.filter(manager=request.user.pk).first()
            == food.restaurant
        )


class CustomerCancellOrder(permissions.BasePermission):
    """
    Check if the customer has the permission to cancell the order.
    """

    message = (
        "Your order has been accepted by the restaurant, you can't cancell it anymore"
    )

    def has_permission(self, request, view):
        order = Order.objects.filter(customer=view.kwargs.get("pk", None)).first()
        return not order.is_accepted
