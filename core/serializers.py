from rest_framework import serializers
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):

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

    def validate(self, attrs):
        if attrs['password'] != attrs['password_repeat']:
            raise serializers.ValidationError('Пароль и повторите пароль не совпадают')
        return attrs

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        user.set_password(validated_data["password"])
        user.save()

        return user
