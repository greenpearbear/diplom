from rest_framework import serializers

from core.serializers import UserSerializer
from goals.models import GoalCategory, Goal


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategoryListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=GoalCategory.objects.all())
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("Категория удалена")
        if value.user != self.context["request"].user:
            return serializers.ValidationError("Нет такой категории")
        return value


class GoalListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"
