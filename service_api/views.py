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


class UserProfile(generics.RetrieveUpdateDestroyAPIView):
    """
    User profile to be retrieved, updated or destroyed.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return User.objects.filter(pk=self.request.user.pk).first()
