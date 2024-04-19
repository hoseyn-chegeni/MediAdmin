from django.urls import path
from .views import (
    TaskCreateView,
    TaskListView,
    TaskUpdateView,
    TaskDeleteView,
    TaskDetailView,
    AssignToMeView,
    AssignToView,
    DoneView,
    DoneNotAsPlannedView,
    InProgressView,
    ReOpenView,
    DeleteSelectedTasksView
)

app_name = "tasks"

urlpatterns = [
    path("list/", TaskListView.as_view(), name="list"),
    path("detail/<int:pk>/", TaskDetailView.as_view(), name="detail"),
    path("create/", TaskCreateView.as_view(), name="create"),
    path("update/<int:pk>/", TaskUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", TaskDeleteView.as_view(), name="delete"),
    path("assign_to_me/<int:pk>", AssignToMeView.as_view(), name="assign_to_me"),
    path("assign_to/<int:pk>", AssignToView.as_view(), name="assign_to"),
    path("done/<int:pk>", DoneView.as_view(), name="done"),
    path(
        "done_not_as_planned/<int:pk>",
        DoneNotAsPlannedView.as_view(),
        name="done_not_as_planned",
    ),
    path("in_progress/<int:pk>", InProgressView.as_view(), name="in_progress"),
    path("reopen/<int:pk>", ReOpenView.as_view(), name="reopen"),
    path(
        "delete/", DeleteSelectedTasksView.as_view(), name="delete_selected_tasks"
    ),
]
