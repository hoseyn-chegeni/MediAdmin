from django.urls import path
from .views import (
    PackageAppointmentDetailViews,
    PackageAppointmentCreateView,
    PackageAppointmentDeleteView,
    PackageAppointmentListView,
    PackageAppointmentUpdateView,
)

app_name = "booking"

urlpatterns = [
    # PACKAGE APPOINTMENT URLS.
    path("package_list/", PackageAppointmentListView.as_view(), name="package_list"),
    path(
        "package_detail/<int:pk>/",
        PackageAppointmentDetailViews.as_view(),
        name="package_detail",
    ),
    path(
        "package_create/", PackageAppointmentCreateView.as_view(), name="package_create"
    ),
    path(
        "package_update/<int:pk>/",
        PackageAppointmentUpdateView.as_view(),
        name="package_update",
    ),
    path(
        "package_delete/<int:pk>/",
        PackageAppointmentDeleteView.as_view(),
        name="package_delete",
    ),
]
