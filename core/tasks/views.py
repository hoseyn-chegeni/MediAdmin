from django.shortcuts import render
from base.views import BaseListView,BaseCreateView,BaseDeleteView,BaseDetailView,BaseUpdateView
from .models import Task
# Create your views here.
class TaskListView(BaseListView):
    model = Task
    template_name = "tasks/list.html"
    context_object_name = "tasks"
    filterset_class = 0
    permission_required = "tasks.view_task"

class TaskDetailView(BaseDetailView):
    model = Task
    template_name = "tasks/detail.html"
    permission_required = "tasks.view_task"

class TaskCreateView(BaseCreateView):
    model = Task
    fields = "__all__"
    template_name = "tasks/create.html"
    app_name = "tasks"
    url_name = "detail"
    permission_required = "tasks.add_task"

class TaskUpdateView(BaseUpdateView):
    model = Task
    fields = "__all__"
    template_name = "tasks/update.html"
    app_name = "tasks"
    url_name = "detail"
    permission_required = "tasks.change_task"

class TaskDeleteView(BaseDeleteView):
    model = Task
    app_name = "tasks"
    url_name = "list"
    permission_required = "tasks.change_task"
