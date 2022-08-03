from django.urls import path
from goals.views import categories, goals, comments, board

urlpatterns = [
    path("goal_category/create", categories.GoalCategoryCreateView.as_view()),
    path("goal_category/list", categories.GoalCategoryListView.as_view()),
    path("goal_category/<pk>", categories.GoalCategoryView.as_view()),
    path("goal/create", goals.GoalCreateView.as_view()),
    path("goal/list", goals.GoalListView.as_view()),
    path("goal/<pk>", goals.GoalView.as_view()),
    path("goal_comment/create", comments.CommentsCreateView.as_view()),
    path("goal_comment/list", comments.CommentsListView.as_view()),
    path("goal_comment/<pk>", comments.CommentsView.as_view()),
    path("board/create", board.BoardCreateView.as_view()),
    path("board/list", board.BoardListView.as_view()),
    path("board/<pk>", board.BoardView.as_view()),

]
