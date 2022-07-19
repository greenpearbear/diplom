from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "password_repeat",
        )

    def validate(self, attrs: dict):
        if attrs['password'] != attrs.pop('password_repeat', None):
            raise serializers.ValidationError('Пароль и повторите пароль не совпадают')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        self.user = user
        return user
