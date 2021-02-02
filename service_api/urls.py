from django.urls import include, path

from service_api import views



urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('users/', views.UserList.as_view()),
]
