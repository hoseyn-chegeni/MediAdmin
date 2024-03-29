from django.urls import path
from .views import (
    PermissionsCreateView,
    PermissionsDeleteView,
    PermissionsDetailView,
    PermissionsListView,
    PermissionsUpdateView,
    AssignPermissionsView,
    GroupCreateView,
    GroupDeleteView,
    GroupDetailView,
    GroupListView,
    GroupUpdateView,
    AssignGroupView,
)

app_name = "permissions"

urlpatterns = [
    path("list/", PermissionsListView.as_view(), name="list"),
    path("detail/<int:pk>/", PermissionsDetailView.as_view(), name="detail"),
    path("create/", PermissionsCreateView.as_view(), name="create"),
    path("update/<int:pk>/", PermissionsUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", PermissionsDeleteView.as_view(), name="delete"),
    path("assign/<int:pk>/", AssignPermissionsView.as_view(), name="assign"),
    # GROUP URLS HERE.
    path("group/list/", GroupListView.as_view(), name="group_list"),
    path("group/detail/<int:pk>/", GroupDetailView.as_view(), name="group_detail"),
    path("group/create/", GroupCreateView.as_view(), name="group_create"),
    path("group/update/<int:pk>/", GroupUpdateView.as_view(), name="group_update"),
    path("group/delete/<int:pk>/", GroupDeleteView.as_view(), name="group_delete"),
    path("group/assign/<int:pk>/", AssignGroupView.as_view(), name="group_assign"),
]
