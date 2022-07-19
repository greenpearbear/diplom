from django.contrib.auth import login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.response import Response

from core.models import User
from core.serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer, \
    UserUpdatePasswordSerializer


class RegistryUserView(CreateAPIView):
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


class LoginUserView(GenericAPIView):

    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        s: UserLoginSerializer = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        user = s.validated_data["user"]
        login(request, user=user)
        user_serializer = UserSerializer(instance=user)
        return Response(user_serializer.data)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class RetrieveUpdateUserView(RetrieveUpdateAPIView):
    model = User
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response({})


class UpdatePasswordUserView(UpdateAPIView):
    model = User
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserUpdatePasswordSerializer

    def get_object(self):
        return self.request.user
