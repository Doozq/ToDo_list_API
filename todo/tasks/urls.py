from django.urls import path
from .views import (
    TaskListCreateView,
    TaskDetailView,
    CommentListCreateView,
    CommentDetailView,
)

urlpatterns = [
    path("", TaskListCreateView.as_view(), name="task-list-create"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path(
        "<int:task_id>/comments/",
        CommentListCreateView.as_view(),
        name="task-comments",
    ),
    path(
        "<int:task_id>/comments/<int:pk>/",
        CommentDetailView.as_view(),
        name="comment-detail",
    ),
]
