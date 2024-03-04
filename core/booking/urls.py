from django.urls import path
from .views import AppointmentCreateView

app_name = "booking"

urlpatterns = [
    path('create/', AppointmentCreateView.as_view(), name = 'create')
]
