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
    pagination_class = LimitOffsetPagination
    ordering_fields = ["priority", "date_deadline"]
    ordering = "-created"
    filterset_fields = ['goal']


class CommentsListView(ListAPIView):
    model = GoalComment
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]


class CommentsView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = CommentsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GoalComment.objects.filter(user=self.request.user, goal__category__is_deleted=False)
