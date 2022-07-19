from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from core.models import User
from core.serializers import UserRegistrationSerializer


class RegistryUser(CreateAPIView):
    model = User
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        super().perform_create(serializer)
        login(
            self.request,
            user=serializer.user,
            backend="django.contrib.auth.backends.ModelBackend",
        )
