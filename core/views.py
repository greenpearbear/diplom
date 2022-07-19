from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from core.models import User
from core.serializers import UserRegistrationSerializer


class RegistryUser(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]