from django.urls import path
from .views import appointments_chart, sessions_per_doctor_chart

app_name = 'charts'

urlpatterns = [
    path('appointments-chart/', appointments_chart, name='appointments_chart'),
    path('sessions-per-doctor-chart/', sessions_per_doctor_chart, name='sessions_per_doctor_chart'),
]