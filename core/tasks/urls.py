from django.urls import path
from .views import (
    TaskCreateView,
    TaskListView,
    TaskUpdateView,
    TaskDeleteView,
    TaskDetailView,
    MyCreatedTaskView,
    MyTaskView
)

app_name = "tasks"

urlpatterns = [
    path("list/", TaskListView.as_view(), name="list"),
    path("detail/<int:pk>/", TaskDetailView.as_view(), name="detail"),
    path("create/", TaskCreateView.as_view(), name="create"),
    path("update/<int:pk>/", TaskUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", TaskDeleteView.as_view(), name="delete"),
    path("my_list/", MyTaskView.as_view(), name="my_list"),
    path("my_created_list/", MyCreatedTaskView.as_view(), name="my_created_list"),

]

