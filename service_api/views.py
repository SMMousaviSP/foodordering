from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.utils import timezone

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from service_api.models import Restaurant, Food, Order
from service_api.serializers import (
    UserSerializer,
    LoginSerializer,
    RestaurantSerializer,
    CreateRestaurantSerializer,
    FoodSerializer,
    PlaceOrderSerializer,
    CancellOrderSerializer,
    ApproveDeliveredOrderSerializer,
    AcceptOrderSerializer,
)
from service_api.permissions import (
    ManagerPermission,
    HasRestaurant,
    IsFoodOwner,
    CustomerCancellOrderPermission,
    IsCustomerOfOrder,
    CustomerApproveDeliveredOrderPermission,
    IsManagerOfOrder,
    ManagerCancellAcceptOrderPermission,
)


class api_login(generics.CreateAPIView):
    """
    Login user with username and password.
    """

    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def api_logout(request):
    request.session.flush()
    return Response(status=status.HTTP_200_OK)


class Register(generics.CreateAPIView):
    """
    Register a new account.
    """

    serializer_class = UserSerializer


class UserList(generics.ListCreateAPIView):
    """
    Show list of all users or create a new user.
    """

    permission_classes = (
        IsAuthenticated,
        IsAdminUser,
    )
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfile(generics.RetrieveUpdateDestroyAPIView):
    """
    User profile to be retrieved, updated or destroyed.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return User.objects.filter(pk=self.request.user.pk).first()


class RestaurantList(generics.ListAPIView):
    """
    List of all restaurants.
    """

    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()


class CreateRestaurant(generics.CreateAPIView):
    """
    Create a restaurant by manager.
    """

    serializer_class = CreateRestaurantSerializer
    permission_classes = (
        IsAuthenticated,
        ManagerPermission,
    )

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)


class ManagerFoodListCreate(generics.ListCreateAPIView):
    """
    Create food for restaurant by manager.
    """

    serializer_class = FoodSerializer
    permission_classes = (
        IsAuthenticated,
        ManagerPermission,
        HasRestaurant,
    )

    def get_queryset(self):
        restaurant = Restaurant.objects.filter(manager=self.request.user.pk).first()
        return Food.objects.filter(restaurant=restaurant)

    def perform_create(self, serializer):
        restaurant = Restaurant.objects.filter(manager=self.request.user.pk).first()
        serializer.save(restaurant=restaurant)


class UpdateFood(generics.UpdateAPIView):
    """
    Update food information and price.
    """

    serializer_class = FoodSerializer
    permission_classes = (
        IsAuthenticated,
        ManagerPermission,
        HasRestaurant,
        IsFoodOwner,
    )
    queryset = Food.objects.all()


class CreateOrder(generics.CreateAPIView):
    """
    Place an Order.
    """

    serializer_class = PlaceOrderSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class CustomerActiveOrderList(generics.ListAPIView):
    """
    List of all active orders which are not cancelled or delivered.
    """

    serializer_class = PlaceOrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(
            customer=self.request.user.pk, is_cancelled=False, is_delivered=False
        )


class CustomerCancelledOrderList(generics.ListAPIView):
    """
    List of customer's cancelled orders.
    """

    serializer_class = PlaceOrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.pk, is_cancelled=True)


class CustomerDeliveredOrderList(generics.ListAPIView):
    """
    List of customer's delivered orders.
    """

    serializer_class = PlaceOrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.pk, is_delivered=True)


class CustomerCancellOrder(generics.UpdateAPIView):
    """
    Cancell order if has permission to.
    """

    serializer_class = CancellOrderSerializer
    permission_classes = (
        IsAuthenticated,
        IsCustomerOfOrder,
        CustomerCancellOrderPermission,
    )
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        serializer.save(cancell_datetime=timezone.now())


class CustomerAprroveDeliveredOrder(generics.UpdateAPIView):
    """
    Aprrove that order has been delivered.
    """

    serializer_class = ApproveDeliveredOrderSerializer
    permission_classes = (
        IsAuthenticated,
        IsCustomerOfOrder,
        CustomerApproveDeliveredOrderPermission,
    )
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        serializer.save(delivered_datetime=timezone.now())


class ManagerActiveOrderList(generics.ListAPIView):
    """
    List of manager's restaurant active orders.
    """

    serializer_class = PlaceOrderSerializer
    permission_classes = (
        IsAuthenticated,
        ManagerPermission,
        HasRestaurant,
    )

    def get_queryset(self):
        restaurant = Restaurant.objects.filter(manager=self.request.user.pk).first()
        foods = Food.objects.filter(restaurant=restaurant.pk).values_list("id").first()
        orders = Order.objects.filter(
            foods__in=foods, is_cancelled=False, is_delivered=False
        )
        return orders


class ManagerCancelledOrderList(generics.ListAPIView):
    """
    List of manager's restaurant cancelled orders.
    """

    serializer_class = PlaceOrderSerializer
    permission_classes = (
        IsAuthenticated,
        ManagerPermission,
        HasRestaurant,
    )

    def get_queryset(self):
        restaurant = Restaurant.objects.filter(manager=self.request.user.pk).first()
        foods = Food.objects.filter(restaurant=restaurant.pk).values_list("id").first()
        orders = Order.objects.filter(
            foods__in=foods, is_cancelled=True
        )
        return orders


class ManagerDeliveredOrderList(generics.ListAPIView):
    """
    List of manager's restaurant delivered orders.
    """

    serializer_class = PlaceOrderSerializer
    permission_classes = (
        IsAuthenticated,
        ManagerPermission,
        HasRestaurant,
    )

    def get_queryset(self):
        restaurant = Restaurant.objects.filter(manager=self.request.user.pk).first()
        foods = Food.objects.filter(restaurant=restaurant.pk).values_list("id").first()
        orders = Order.objects.filter(
            foods__in=foods, is_delivered=True
        )
        return orders


class ManagerCancellOrder(generics.UpdateAPIView):
    """
    Cancell order if has permission to.
    """

    serializer_class = CancellOrderSerializer
    permission_classes = (
        IsAuthenticated,
        IsManagerOfOrder,
        ManagerCancellAcceptOrderPermission,
    )
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        serializer.save(cancell_datetime=timezone.now())


class ManagerAcceptOrder(generics.UpdateAPIView):
    """
    Accept order if has permission to.
    """

    serializer_class = AcceptOrderSerializer
    permission_classes = (
        IsAuthenticated,
        IsManagerOfOrder,
        ManagerCancellAcceptOrderPermission,
    )
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        serializer.save(accept_datetime=timezone.now())
