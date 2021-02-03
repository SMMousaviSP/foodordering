from django.urls import include, path
from django.views.generic import TemplateView

from rest_framework.schemas import get_schema_view

from service_api import views


urlpatterns = [
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
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
    path("register/", views.Register.as_view()),
    path("login/", views.api_login.as_view()),
    path("logout/", views.api_logout),
    path("users/", views.UserList.as_view()),
    path("profile/", views.UserProfile.as_view()),
    path("restaurants/", views.RestaurantList.as_view()),
    path("newrestaurant/", views.CreateRestaurant.as_view()),
    path("managerfoods/", views.ManagerFoodListCreate.as_view()),
]
