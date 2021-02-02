from django.urls import include, path
from django.views.generic import TemplateView

from rest_framework.schemas import get_schema_view

from service_api import views


urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui/swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),

    path('login/', views.api_login),
    path('logout/', views.api_logout),
    path('users/', views.UserList.as_view()),
    path('profile/', views.UserProfile.as_view()),
]
