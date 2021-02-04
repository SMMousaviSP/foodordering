from django.urls import include, path
from django.views.generic import TemplateView

from rest_framework.schemas import get_schema_view

from service_api import views


CUSTOMER_PREFIX = "customer"
MANAGER_PREFIX = "manager"

urlpatterns = [
    # rest_framework Authentication
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # OpenAPI and Swagger UI for API documentations
    path(
        "openapi",
        get_schema_view(
            title="Food Ordering Service API",
            description="API documentation for every accessable url to you",
            version="1.0.0",
        ),
        name="openapi-schema",
    ),
    path(
        "documentation/",
        TemplateView.as_view(
            template_name="swagger-ui/swagger-ui.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="swagger-ui",
    ),
    # General API URI
    path("register/", views.Register.as_view()),
    path("login/", views.api_login.as_view()),
    path("logout/", views.api_logout),
    path("users/", views.UserList.as_view()),
    path("profile/", views.UserProfile.as_view()),
    path("restaurants/", views.RestaurantList.as_view()),
    # Managers API URI
    path(f"{MANAGER_PREFIX}/newrestaurant/", views.CreateRestaurant.as_view()),
    path(f"{MANAGER_PREFIX}/foods/", views.ManagerFoodListCreate.as_view()),
    path(f"{MANAGER_PREFIX}/updatefood/<int:pk>/", views.UpdateFood.as_view()),
    path(f"{MANAGER_PREFIX}/activeorders/", views.ManagerActiveOrderList.as_view()),
    path(
        f"{MANAGER_PREFIX}/cancelledorders/",
        views.ManagerCancelledOrderList.as_view(),
    ),
    path(
        f"{MANAGER_PREFIX}/deliveredorders/",
        views.ManagerDeliveredOrderList.as_view(),
    ),
    path(f"{MANAGER_PREFIX}/cancell/<int:pk>/", views.ManagerCancellOrder.as_view()),
    # Customers API URI
    path(f"{CUSTOMER_PREFIX}/neworder/", views.CreateOrder.as_view()),
    path(f"{CUSTOMER_PREFIX}/activeorders/", views.CustomerActiveOrderList.as_view()),
    path(
        f"{CUSTOMER_PREFIX}/cancelledorders/",
        views.CustomerCancelledOrderList.as_view(),
    ),
    path(
        f"{CUSTOMER_PREFIX}/deliveredorders/",
        views.CustomerDeliveredOrderList.as_view(),
    ),
    path(f"{CUSTOMER_PREFIX}/cancell/<int:pk>/", views.CustomerCancellOrder.as_view()),
    path(
        f"{CUSTOMER_PREFIX}/approvedelivered/<int:pk>/",
        views.CustomerAprroveDeliveredOrder.as_view(),
    ),
]
