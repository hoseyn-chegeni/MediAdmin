from django.shortcuts import render
from django.contrib.auth.models import Permission, Group
from base.views import (
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseUpdateView,
    BaseListView,
)
from django.views.generic import ListView
from accounts.models import User


# Create your views here.
class PermissionsListView(ListView):
    model = Permission
    template_name = "permission/list.html"
    context_object_name = "permission"


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


