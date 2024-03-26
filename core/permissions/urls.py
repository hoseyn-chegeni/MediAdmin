from django.urls import path
from .views import (
    PermissionsCreateView,
    PermissionsDeleteView,
    PermissionsDetailView,
    PermissionsListView,
    PermissionsUpdateView,
    AssignPermissionsView,
)

app_name = "permissions"

urlpatterns = [
    path("list/", PermissionsListView.as_view(), name="list"),
    path("detail/<int:pk>/", PermissionsDetailView.as_view(), name="detail"),
    path("create/", PermissionsCreateView.as_view(), name="create"),
    path("update/<int:pk>/", PermissionsUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", PermissionsDeleteView.as_view(), name="delete"),
    path("assign/<int:pk>/", AssignPermissionsView.as_view(), name="assign"),
]
