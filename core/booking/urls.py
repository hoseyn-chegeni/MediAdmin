from django.urls import path
from .views import (
    AppointmentCreateView,
    AppointmentDeleteView,
    AppointmentDetailView,
    AppointmentListView,
    AppointmentUpdateView,
    PackageAppointmentDetailViews,
    PackageAppointmentCreateView,
    PackageAppointmentDeleteView,
    PackageAppointmentListView,
    PackageAppointmentUpdateView,
    TodaysAppointmentListView,
)

app_name = "booking"

urlpatterns = [
    path("list/", AppointmentListView.as_view(), name="list"),
    path("today_list/", TodaysAppointmentListView.as_view(), name="today_list"),
    path("detail/<int:pk>/", AppointmentDetailView.as_view(), name="detail"),
    path("create/", AppointmentCreateView.as_view(), name="create"),
    path("update/<int:pk>/", AppointmentUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", AppointmentDeleteView.as_view(), name="delete"),
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
