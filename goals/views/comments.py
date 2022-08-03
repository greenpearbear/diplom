from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination

from goals.models import Goal, GoalComment
from goals.serializers import CommentsCreateSerializer, CommentsSerializer


class CommentsCreateView(CreateAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentsCreateSerializer


class CommentsListView(ListAPIView):
    model = GoalComment
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["goal"]
    ordering_filed = "created"

    def get_queryset(self):
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user,
                                          goal__category__is_deleted=False)


class CommentsView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalComment.objects.filter(goal__category__board__participants__user=self.request.user,
                                          goal__category__is_deleted=False)
