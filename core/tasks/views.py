from django.shortcuts import render, HttpResponseRedirect, redirect
from base.views import (
    BaseListView,
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseUpdateView,
)
from .models import Task
from .filters import TaskFilter
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


# Create your views here.
class TaskListView(BaseListView):
    model = Task
    template_name = "tasks/list.html"
    context_object_name = "tasks"
    filterset_class = TaskFilter
    permission_required = "tasks.view_task"


class TaskDetailView(BaseDetailView):
    model = Task
    template_name = "tasks/detail.html"
    permission_required = "tasks.view_task"


class TaskCreateView(BaseCreateView):
    model = Task
    fields = [
        "title",
        "description",
        "type",
        "priority",
        "assign_to",
    ]
    template_name = "tasks/create.html"
    app_name = "tasks"
    url_name = "detail"
    permission_required = "tasks.add_task"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.status = "در انتظار بررسی"
        return super().form_valid(form)


class TaskUpdateView(BaseUpdateView):
    model = Task
    fields = [
        "title",
        "description",
        "type",
        "priority",
        "assign_to",
    ]
    template_name = "tasks/update.html"
    app_name = "tasks"
    url_name = "detail"
    permission_required = "tasks.change_task"


class TaskDeleteView(BaseDeleteView):
    model = Task
    app_name = "tasks"
    url_name = "list"
    permission_required = "tasks.change_task"


class MyTaskView(BaseListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/my_task.html"
    filterset_class = TaskFilter
    permission_required = "tasks.view_task"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(assign_to_id=self.request.user.id)


class MyCreatedTaskView(BaseListView):
    template_name = "tasks/my_created_task.html"
    model = Task
    context_object_name = "tasks"
    filterset_class = TaskFilter
    permission_required = "tasks.view_task"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(created_by_id=self.request.user.id)


class AssignToMeView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = Task.objects.filter(pk=pk).first()
        if task and task.status == "در انتظار بررسی":
            task.assign_to = self.request.user
            messages.success(
                self.request, f"تسک {task.id} با موفقیت به شما اختصاص داده شد ."
            )
            task.save()

        return HttpResponseRedirect(
            reverse_lazy("tasks:detail", kwargs={"pk": task.pk})
        )


class AssignToView(BaseUpdateView):
    template_name = "tasks/assign_to.html"
    model = Task
    fields = ("assign_to",)
    permission_required = "tasks.change_task"
    app_name = "tasks"
    url_name = "detail"


class DoneView(BaseUpdateView):
    template_name = "tasks/done.html"
    model = Task
    fields = ("answer",)
    permission_required = "tasks.change_task"
    app_name = "tasks"
    url_name = "detail"

    def form_valid(self, form):
        form.instance.status = "انجام شده"
        return super().form_valid(form)


class DoneNotAsPlannedView(BaseUpdateView):
    template_name = "tasks/done.html"
    model = Task
    fields = ("answer",)
    permission_required = "tasks.change_task"
    app_name = "tasks"
    url_name = "detail"

    def form_valid(self, form):
        form.instance.status = "لغو شده"
        return super().form_valid(form)


class InProgressView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = Task.objects.filter(pk=pk).first()
        if task and task.status == "در انتظار بررسی":
            task.status = "در حال انجام"
            messages.success(
                self.request,
                f" وضعیت تسک {task.id} یا موفقیت به حالت در حال انجام تغییر داده شد",
            )
            task.save()

        return HttpResponseRedirect(
            reverse_lazy("tasks:detail", kwargs={"pk": task.pk})
        )


class ReOpenView(BaseUpdateView):
    template_name = "tasks/reopen.html"
    model = Task
    fields = ("reopen_message",)
    permission_required = "tasks.change_task"
    app_name = "tasks"
    url_name = "detail"

    def form_valid(self, form):
        form.instance.status = "در انتظار بررسی"
        form.instance.assign_to = None
        return super().form_valid(form)


class DeleteSelectedTasksView(View):
    def post(self, request):
        if request.method == "POST":
            tasks_ids = request.POST.getlist(
                "tasks_ids"
            )  # Get the list of selected user IDs from the form
            Task.objects.filter(id__in=tasks_ids).delete()  # Delete selected users
        return redirect("tasks:list")