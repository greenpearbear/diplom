from rest_framework import serializers
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, unique=True)

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        user.set_password(validated_data["password"])
        user.save()

        return user

    def validate(self, attrs):
        if attrs['password'] != attrs['password_repeat']:
            raise serializers.ValidationError('Пароль и ')
