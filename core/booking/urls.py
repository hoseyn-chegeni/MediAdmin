from django.urls import path
from .views import (
    AppointmentCreateView,
    AppointmentDeleteView,
    AppointmentDetailView,
    AppointmentListView,
    AppointmentUpdateView,
    PackageAppointmentDetailViews,
)

app_name = "booking"

urlpatterns = [
    path("list/", AppointmentListView.as_view(), name="list"),
    path("detail/<int:pk>/", AppointmentDetailView.as_view(), name="detail"),
    path("create/", AppointmentCreateView.as_view(), name="create"),
    path("update/<int:pk>/", AppointmentUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", AppointmentDeleteView.as_view(), name="delete"),
    path("package_detail/<int:pk>/", PackageAppointmentDetailViews.as_view(), name="package_detail"),

]
