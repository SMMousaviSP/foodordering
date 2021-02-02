from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from service_api.serializers import UserSerializer


class UserList(generics.ListCreateAPIView):
    """
    Show list of all users or create a new user.
    """
    permission_classes = (IsAuthenticated, IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
