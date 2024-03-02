from django.urls import path
from .views import (
    DoctorCreateView,
    DoctorListView,
    DoctorUpdateView,
    DoctorDeleteView,
    DoctorDetailView,
    SuspendDoctorListView,
    SuspendDoctorView,
    ReactiveDoctorView,
)

app_name = "doctor"

urlpatterns = [
    path("doctor/list/", DoctorListView.as_view(), name="list"),
    path("doctor/suspend_list/", SuspendDoctorListView.as_view(), name="suspend_list"),
    path("doctor/detail/<int:pk>/", DoctorDetailView.as_view(), name="detail"),
    path("doctor/create/", DoctorCreateView.as_view(), name="create"),
    path("doctor/update/<int:pk>/", DoctorUpdateView.as_view(), name="update"),
    path("doctor/delete/<int:pk>/", DoctorDeleteView.as_view(), name="delete"),
    path("suspend/<int:pk>/", SuspendDoctorView.as_view(), name="suspend"),
    path("reactive/<int:pk>/", ReactiveDoctorView.as_view(), name="reactive"),
]
