from django.shortcuts import render
from django.contrib.auth.models import Permission, Group
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseUpdateView,
    BaseListView,
)
from accounts.models import User
from .filters import PermissionFilters, GroupFilter
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.
class PermissionsListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = Permission
    template_name = "permission/list.html"
    context_object_name = "permission"
    filterset_class = PermissionFilters
    permission_required = "permission.add_permission"


class PermissionsDetailView(BaseDetailView):
    model = Permission
    template_name = "permission/detail.html"
    permission_required = "permission.view_permission"


class PermissionsCreateView(BaseCreateView):
    model = Permission
    template_name = "permission/create.html"
    permission_required = "permission.add_permission"
    fields = "__all__"
    app_name = "permissions"
    url_name = "detail"


class PermissionsUpdateView(BaseUpdateView):
    model = Permission
    template_name = "permission/update.html"
    permission_required = "permission.change_permission"
    fields = "__all__"
    app_name = "permissions"
    url_name = "detail"


class PermissionsDeleteView(BaseDeleteView):
    model = Permission
    permission_required = "permission.delete_permission"
    app_name = "permissions"
    url_name = "list"


class AssignPermissionsView(BaseUpdateView):
    model = User
    fields = ("user_permissions",)
    template_name = "permission/assign.html"
    permission_required = "auth.change_user"
    app_name = "accounts"
    url_name = "user_detail"


# GROUP VIEWS HERE.
class GroupListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = Group
    template_name = "permission/group/list.html"
    context_object_name = "group"
    filterset_class = GroupFilter
    permission_required = "auth.view_group"


class GroupDetailView(BaseDetailView):
    model = Group
    template_name = "permission/group/detail.html"
    permission_required = "auth.view_group"


class GroupCreateView(BaseCreateView):
    model = Group
    template_name = "permission/group/create.html"
    permission_required = "auth.add_group"
    fields = "__all__"
    app_name = "permissions"
    url_name = "group_detail"


class GroupUpdateView(BaseUpdateView):
    model = Group
    template_name = "permission/group/update.html"
    permission_required = "permission.change_permission"
    fields = "__all__"
    app_name = "permissions"
    url_name = "group_detail"


class GroupDeleteView(BaseDeleteView):
    model = Group
    permission_required = "auth.delete_group"
    app_name = "permissions"
    url_name = "group_list"


class AssignGroupView(BaseUpdateView):
    model = User
    fields = ("groups",)
    template_name = "permission/group/assign.html"
    permission_required = "auth.change_user"
    app_name = "accounts"
    url_name = "user_detail"
