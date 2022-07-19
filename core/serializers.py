from django.contrib.auth import authenticate
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


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs: dict):
        username = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("username or password is incorrect")
        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
        )


class UserUpdatePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(
        write_only=True, validators=[validate_password]
    )

    class Meta:
        model = User
        read_only_fields = ("id",)
        fields = ("old_password", "new_password")

    def validate(self, attrs):
        old_password = attrs.get("old_password")
        user: User = self.instance
        if not user.check_password(old_password):
            raise serializers.ValidationError({"old_password": "field is incorrect"})
        return attrs

    def update(self, instance: User, validated_data):
        instance.set_password(validated_data["new_password"])
        instance.save(update_fields=["password"])
        return instance
